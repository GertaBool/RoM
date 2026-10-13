// Minimal DOM for the engine's FXml interface (headless harness).
#pragma once
#include <string>
#include <vector>
#include <map>

struct XNode
{
	std::string tag;            // element name; "#doc" for the document node
	std::wstring text;          // concatenated character data of this element
	std::vector<XNode*> kids;   // element children only (comments are dropped)
	XNode* parent;
	int index;                  // position in parent->kids
	XNode() : parent(0), index(0) {}
	~XNode() { for (size_t i = 0; i < kids.size(); ++i) delete kids[i]; }
};

class XDoc
{
public:
	XDoc() : root(0), cur(0) {}
	~XDoc() { delete root; }
	bool load(const std::string& path, std::string& err);
	XNode* root;
	XNode* cur;
	std::map<std::string, std::string> types;   // element name -> schema dt:type
	std::string path;
};

std::wstring textOf(const XNode* n);       // element text including descendants
std::string narrow(const std::wstring& w); // Latin-1 narrowing, '?' otherwise
