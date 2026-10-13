// XML parser for the headless harness: enough of XML 1.0 for Civ4 asset files.
#include "xmldom.h"
#include <cstdio>
#include <cstring>
#include <cstdlib>

namespace
{
	bool readFile(const std::string& p, std::string& out)
	{
		FILE* f = fopen(p.c_str(), "rb");
		if (!f) return false;
		char buf[65536];
		size_t n;
		while ((n = fread(buf, 1, sizeof(buf), f)) > 0) out.append(buf, n);
		fclose(f);
		return true;
	}

	// Decode bytes to UTF-16 code units (BMP only), honouring the declared encoding.
	std::wstring decode(const std::string& s)
	{
		bool utf8 = true;
		size_t decl = s.find("<?xml");
		if (decl != std::string::npos)
		{
			size_t end = s.find("?>", decl);
			std::string head = s.substr(decl, end == std::string::npos ? 0 : end - decl);
			for (size_t i = 0; i < head.size(); ++i) head[i] = (char)tolower(head[i]);
			if (head.find("iso-8859-1") != std::string::npos || head.find("windows-1252") != std::string::npos)
				utf8 = false;
		}
		std::wstring w;
		w.reserve(s.size());
		size_t i = 0;
		if (s.size() >= 3 && (unsigned char)s[0] == 0xEF && (unsigned char)s[1] == 0xBB && (unsigned char)s[2] == 0xBF) i = 3;
		for (; i < s.size(); ++i)
		{
			unsigned char c = (unsigned char)s[i];
			if (!utf8 || c < 0x80) { w += (wchar_t)c; continue; }
			int extra = (c >= 0xF0) ? 3 : (c >= 0xE0) ? 2 : (c >= 0xC0) ? 1 : 0;
			if (extra == 0 || i + extra >= s.size() + 0) { w += (wchar_t)c; continue; }
			unsigned int cp = c & (0x3F >> extra);
			bool ok = true;
			for (int k = 1; k <= extra; ++k)
			{
				if (i + k >= s.size()) { ok = false; break; }
				unsigned char cc = (unsigned char)s[i + k];
				if ((cc & 0xC0) != 0x80) { ok = false; break; }
				cp = (cp << 6) | (cc & 0x3F);
			}
			if (!ok) { w += (wchar_t)c; continue; }   // malformed: treat as Latin-1 byte
			i += extra;
			w += (wchar_t)(cp > 0xFFFF ? '?' : cp);
		}
		return w;
	}

	void appendEntity(const std::wstring& ent, std::wstring& out)
	{
		if (ent == L"amp") out += L'&';
		else if (ent == L"lt") out += L'<';
		else if (ent == L"gt") out += L'>';
		else if (ent == L"quot") out += L'"';
		else if (ent == L"apos") out += L'\'';
		else if (!ent.empty() && ent[0] == L'#')
		{
			unsigned long v = (ent.size() > 1 && (ent[1] == L'x' || ent[1] == L'X'))
				? wcstoul(ent.c_str() + 2, 0, 16) : wcstoul(ent.c_str() + 1, 0, 10);
			out += (wchar_t)(v > 0xFFFF ? '?' : v);
		}
		else { out += L'&'; out += ent; out += L';'; }
	}

	struct Parser
	{
		const std::wstring& s;
		size_t p;
		std::string err;
		std::string schemaName;
		Parser(const std::wstring& src) : s(src), p(0) {}

		bool startsWith(const wchar_t* t) const { return s.compare(p, wcslen(t), t) == 0; }
		void skipWs() { while (p < s.size() && iswspace(s[p])) ++p; }
		bool skipPast(const wchar_t* t)
		{
			size_t q = s.find(t, p);
			if (q == std::wstring::npos) return false;
			p = q + wcslen(t);
			return true;
		}
		std::wstring name()
		{
			size_t b = p;
			while (p < s.size() && !iswspace(s[p]) && s[p] != L'>' && s[p] != L'/' && s[p] != L'=') ++p;
			return s.substr(b, p - b);
		}
		void text(std::wstring& out, wchar_t stop)
		{
			while (p < s.size() && s[p] != stop)
			{
				if (s[p] == L'&')
				{
					size_t e = s.find(L';', p);
					if (e == std::wstring::npos) { out += s[p++]; continue; }
					appendEntity(s.substr(p + 1, e - p - 1), out);
					p = e + 1;
				}
				else out += s[p++];
			}
		}
		// Parse children of `parent` until its end tag (or EOF for the document).
		bool content(XNode* parent)
		{
			while (p < s.size())
			{
				if (startsWith(L"<!--")) { if (!skipPast(L"-->")) return fail("unterminated comment"); continue; }
				if (startsWith(L"<?")) { if (!skipPast(L"?>")) return fail("unterminated PI"); continue; }
				if (startsWith(L"<![CDATA["))
				{
					p += 9;
					size_t e = s.find(L"]]>", p);
					if (e == std::wstring::npos) return fail("unterminated CDATA");
					parent->text += s.substr(p, e - p);
					p = e + 3;
					continue;
				}
				if (startsWith(L"<!")) { if (!skipPast(L">")) return fail("unterminated declaration"); continue; }
				if (startsWith(L"</"))
				{
					p += 2;
					std::wstring n = name();
					skipPast(L">");
					std::string nn(narrow(n));
					if (nn != parent->tag) return fail("mismatched end tag </" + nn + "> for <" + parent->tag + ">");
					return true;
				}
				if (s[p] == L'<')
				{
					++p;
					XNode* n = new XNode;
					n->tag = narrow(name());
					n->parent = parent;
					n->index = (int)parent->kids.size();
					parent->kids.push_back(n);
					bool selfClosed = false;
					for (;;)
					{
						skipWs();
						if (p >= s.size()) return fail("EOF in tag");
						if (s[p] == L'/') { selfClosed = true; ++p; skipWs(); if (s[p] == L'>') ++p; break; }
						if (s[p] == L'>') { ++p; break; }
						std::wstring an = name();
						skipWs();
						std::wstring av;
						if (p < s.size() && s[p] == L'=')
						{
							++p; skipWs();
							wchar_t q = s[p++];
							text(av, q);
							++p;
						}
						if (an == L"xmlns" && av.compare(0, 9, L"x-schema:") == 0) schemaName = narrow(av.substr(9));
					}
					if (!selfClosed && !content(n)) return false;
					continue;
				}
				text(parent->text, L'<');
			}
			if (parent->tag != "#doc") return fail("EOF before </" + parent->tag + ">");
			return true;
		}
		bool fail(const std::string& m) { err = m; return false; }
	};

	void trim(std::wstring& w)
	{
		size_t b = 0, e = w.size();
		while (b < e && iswspace(w[b])) ++b;
		while (e > b && iswspace(w[e - 1])) --e;
		w = w.substr(b, e - b);
	}
	void trimAll(XNode* n)
	{
		trim(n->text);
		for (size_t i = 0; i < n->kids.size(); ++i) trimAll(n->kids[i]);
	}

	// Collect <ElementType name="x" ... dt:type="int"/> declarations.
	void readSchema(const std::string& path, std::map<std::string, std::string>& types)
	{
		std::string raw;
		if (!readFile(path, raw)) return;
		size_t p = 0;
		while ((p = raw.find("<ElementType", p)) != std::string::npos)
		{
			size_t e = raw.find('>', p);
			std::string t = raw.substr(p, e - p);
			size_t n = t.find("name=\"");
			size_t d = t.find("dt:type=\"");
			if (n != std::string::npos && d != std::string::npos)
			{
				n += 6; d += 9;
				types[t.substr(n, t.find('"', n) - n)] = t.substr(d, t.find('"', d) - d);
			}
			p = e;
		}
	}
}

std::string narrow(const std::wstring& w)
{
	std::string s(w.size(), ' ');
	for (size_t i = 0; i < w.size(); ++i) s[i] = (char)(w[i] < 256 ? w[i] : '?');
	return s;
}

std::wstring textOf(const XNode* n)
{
	std::wstring t = n->text;
	for (size_t i = 0; i < n->kids.size(); ++i) t += textOf(n->kids[i]);
	return t;
}

bool XDoc::load(const std::string& p, std::string& err)
{
	std::string raw;
	if (!readFile(p, raw)) { err = "cannot open"; return false; }
	std::wstring w = decode(raw);
	Parser ps(w);
	XNode* doc = new XNode;
	doc->tag = "#doc";
	if (!ps.content(doc)) { err = ps.err; delete doc; return false; }
	trimAll(doc);
	delete root;
	root = doc;
	cur = doc;
	path = p;
	types.clear();
	if (!ps.schemaName.empty())
	{
		std::string dir = p.substr(0, p.find_last_of("\\/") + 1);
		readSchema(dir + ps.schemaName, types);
	}
	return true;
}
