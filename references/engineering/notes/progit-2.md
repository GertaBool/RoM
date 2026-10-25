# Chacon & Straub, Pro Git, 2nd ed., chapters 7 (parts), 8.3, 10 (Apress, 2nd ed.; PDF version 2.1.449, 2025-12-12)
Source: lit3/progit/doc.txt. Read: lines 9303-11184 (ch. 7: Rewriting History, Reset Demystified, Advanced Merging, Rerere, Debugging with Git), 13451-13991 (ch. 8.3 Git Hooks and 8.4 An Example Git-Enforced Policy), 16350-18261 (ch. 10 Git Internals in full, including Environment Variables, and the opening of Appendix A on graphical interfaces).

## What it says

### Rewriting History (7.6)
- p. 249 (Rewriting History): "you can rewrite commits that already happened so they look like they happened in a different way" -- reordering, rewording, squashing, splitting or removing commits, all before sharing.
- p. 249 (Don't push your work until you're happy with it): "you should consider pushed work as final unless you have good reason to change it" -- the cardinal rule: rewrite freely only while the work is local.
- p. 250 (Changing the Last Commit): "You need to be careful with this technique because amending changes the SHA-1 of the commit" -- amend is a small rebase; do not amend a pushed commit.
- p. 250 (An amended commit may need an amended commit message): "If you amend the content of the commit substantially, you should almost certainly update the commit message to reflect that amended content." -- for trivial fixes, git commit --amend --no-edit keeps the message.
- p. 250 (Changing Multiple Commit Messages): "Don't include any commit you've already pushed to a central server" -- every commit in the rebased range and all descendants are rewritten, giving others an alternate version of the same change.
- p. 251 (Changing Multiple Commit Messages): "It's important to note that these commits are listed in the opposite order than you normally see them using the log command." -- the interactive rebase list is a script, oldest first, replayed top to bottom.
- p. 251 (rebase script help text): "If you remove a line here THAT COMMIT WILL BE LOST." -- the todo list also offers reword, edit, squash, fixup, exec, break, drop, label, reset and merge.
- p. 253 (Squashing Commits): "Git applies both that change and the change directly before it and makes you merge the commit messages together" -- squash melds a commit into the previous one.
- p. 254 (Splitting a Commit): "Splitting a commit undoes a commit and then partially stages and commits as many times as commits you want to end up with." -- mark it edit, git reset HEAD^, then stage and commit pieces and git rebase --continue.
- p. 255 (Splitting a Commit): "make sure no changed commit shows up in that list that you've already pushed to a shared repository" -- the split changes the SHA-1s of the commits after it.
- p. 255 (Deleting a commit): "deleting or altering a commit will cause the rewriting of all the commits that follow it" -- the further back, the more commits recreated and the more possible conflicts.
- p. 255 (Deleting a commit): "Type git rebase --abort, and your repo will be returned to the state it was in before you started the rebase." -- after a finished rebase, git reflog recovers the earlier branch.
- p. 255 (The Nuclear Option: filter-branch): "git filter-branch has many pitfalls, and is no longer the recommended way to rewrite history" -- the authors recommend git-filter-repo instead.
- p. 256 (Removing a File from Every Commit): "It's generally a good idea to do this in a testing branch and then hard-reset your master branch after you've determined the outcome is what you really want." -- --tree-filter runs a command after each checkout and recommits.
- p. 257 (Changing Email Addresses Globally): "this command changes every commit SHA-1 in your history, not just those that have the matching email address" -- because commits contain their parents' SHA-1s.

### Reset Demystified (7.7)
- p. 257 (The Three Trees): "Git as a system manages and manipulates three trees in its normal operation" -- HEAD (last commit snapshot, next parent), Index (proposed next commit snapshot), Working Directory (sandbox).
- p. 258 (The Index): "The index is your proposed next commit." -- also called the staging area; technically a flattened manifest, not a tree.
- p. 258 (The Working Directory): "Think of the working directory as a sandbox, where you can try changes out before committing them to your staging area (index) and then to history."
- p. 265 (The Workflow): "When you checkout a branch, it changes HEAD to point to the new branch ref, populates your index with the snapshot of that commit, then copies the contents of the index into your working directory."
- p. 266 (Step 1: Move HEAD): "reset moves the branch that HEAD is pointing to" -- unlike checkout, which changes HEAD itself.
- p. 267 (Step 1: Move HEAD): "With reset --soft, it will simply stop there." -- this undoes the last git commit without touching index or working directory.
- p. 268 (Step 2: Updating the Index (--mixed)): "This is also the default, so if you specify no option at all" -- the mixed reset also unstages everything.
- p. 269 (Step 3: Updating the Working Directory (--hard)): "this flag (--hard) is the only way to make the reset command dangerous, and one of the very few cases where Git will actually destroy data" -- uncommitted work it overwrites is unrecoverable.
- p. 269 (Recap): "The reset command overwrites these three trees in a specific order, stopping when you tell it to" -- move the branch, make the index look like HEAD, make the working directory look like the index.
- p. 270 (Reset With a Path): "If you specify a path, reset will skip step 1, and limit the remainder of its actions to a specific file or set of files." -- git reset file.txt unstages the file, the exact opposite of git add.
- p. 272 (Reset With a Path): "the reset command will accept a --patch option to unstage content on a hunk-by-hunk basis"
- p. 272 (Squashing): "You can use reset to quickly and easily squash them into a single commit" -- git reset --soft HEAD~2 followed by git commit.
- p. 276 (Check It Out, Without Paths): "unlike reset --hard, checkout is working-directory safe; it will check to make sure it's not blowing away files that have changes to them"
- p. 276 (Check It Out, Without Paths): "reset will move the branch HEAD points to, checkout moves HEAD itself."
- p. 277 (With Paths): "it's not working-directory safe, and it does not move HEAD" -- checkout with a path overwrites the file in the working directory.
- p. 277 (Summary): "Pay especial attention to the 'WD Safe?' column" -- the cheat-sheet marks reset --hard [commit] and checkout [commit] <paths> as not working-directory safe.

### Advanced Merging (7.8)
- p. 277 (Advanced Merging): "you can keep it up to date as you go, solving small conflicts often, rather than be surprised by one enormous conflict at the end of the series"
- p. 277 (Advanced Merging): "if there is a conflict, it does not try to be clever about automatically resolving it" -- so waiting too long to merge fast-diverging branches causes trouble.
- p. 278 (Merge Conflicts): "try to make sure your working directory is clean before doing a merge that may have conflicts" -- commit work in progress to a temporary branch or stash it so anything can be undone.
- p. 278 (Merge Conflicts): "change all the Unix line endings to DOS line endings, essentially changing every line of the file, but just with whitespace" -- the worked example of a whitespace-only change that makes a merge conflict.
- p. 280 (Aborting a Merge): "The git merge --abort option tries to revert back to your state before you ran the merge." -- it may fail only with unstashed, uncommitted changes present.
- p. 280 (Ignoring Whitespace): "every line is removed on one side and added again on the other" -- the sign of a whitespace conflict; -Xignore-all-space or -Xignore-space-change let the merge through.
- p. 281 (Manual File Re-merging): "Stage 1 is the common ancestor, stage 2 is your version and stage 3 is from the MERGE_HEAD" -- extracted with git show :1:file etc., or ls-files -u for blob SHA-1s.
- p. 282 (Manual File Re-merging): "In the ignore-space-change merge, we actually ended up with a few lines with DOS line endings, making things mixed." -- running dos2unix on their side and git merge-file fixes the whitespace before the merge instead.
- p. 282 (Manual File Re-merging): "to see what the merge introduced, you can run git diff --ours" -- --theirs and --base compare the result to the other stages.
- p. 284 (Checking Out Conflicts): "If you pass it diff3, Git will use a slightly different version of conflict markers" -- shows the base version inline; can be made the default with merge.conflictstyle diff3.
- p. 285 (Checking Out Conflicts): "The git checkout command can also take --ours and --theirs options" -- a fast way to pick one side, useful for binary files.
- p. 285 (Merge Log): "Reviewing a little bit of history to remember why two lines of development were touching the same area of code can be really helpful sometimes." -- git log --left-right HEAD...MERGE_HEAD, and --merge to limit to conflicted files.
- p. 286 (Combined Diff Format): "when you run git diff while in a conflicted merge state, you only get what is currently still in conflict"
- p. 287 (Combined Diff Format): "Git will output this format if you run git show on a merge commit" -- or git log --cc -p, to see after the fact how a merge was resolved.
- p. 288 (Fix the references): "If the unwanted merge commit only exists on your local repository, the easiest and best solution is to move the branches so that they point where you want them to."
- p. 289 (Fix the references): "if other people have the commits you're rewriting, you should probably avoid reset" -- it also loses any commits made since the merge.
- p. 289 (Reverse the commit): "The -m 1 flag indicates which parent is the" -- git revert -m 1 HEAD makes a new commit undoing the merge while keeping parent 1 (the mainline).
- p. 290 (Reverse the commit): "Git will get confused if you try to merge topic into master again" -- the reverted commits remain in history, so a later merge brings in only newer changes.
- p. 290 (Reverse the commit): "The best way around this is to un-revert the original merge" -- revert the revert, then merge again.
- p. 291 (Our or Theirs Preference): "Any differences that conflict, it will simply choose the side you specify in whole, including binary files." -- -Xours or -Xtheirs, no conflict markers.
- p. 292 (Our or Theirs Preference): "It will record a new merge commit with both branches as parents, but it will not even look at the branch you're merging in." -- the -s ours strategy, a fake merge, e.g. to mark a backported fix as already merged.
- p. 292 (Subtree Merging): "you have two projects, and one of the projects maps to a subdirectory of the other one" -- read-tree --prefix plus merge -Xsubtree.
- p. 294 (Subtree Merging): "it's a bit more complex and easier to make mistakes in reintegrating changes or accidentally pushing a branch into an unrelated repository" -- diffs need git diff-tree.

### Rerere (7.9)
- p. 294 (Rerere): "it allows you to ask Git to remember how you've resolved a hunk conflict so that the next time it sees the same conflict, Git can resolve it for you automatically" -- reuse recorded resolution.
- p. 295 (Rerere): "This same tactic can be used if you want to keep a branch rebased so you don't have to deal with the same rebasing conflicts each time you do it." -- also for test merges of many topic branches that are rewound.
- p. 295 (Rerere): "$ git config --global rerere.enabled true"
- p. 296 (Rerere): "You should notice the new line Recorded preimage for FILE in there." -- git rerere status and git rerere diff show what is recorded.
- p. 299 (Rerere): "take a look at the Resolved FILE using previous resolution line" -- on the later rebase the file arrives already resolved, without markers.
- p. 301 (Rerere): "if you do a lot of re-merges, or want to keep a topic branch up to date with your master branch without a ton of merges, or you rebase often, you can turn on rerere"

### Debugging with Git (7.10)
- p. 301 (File Annotation): "It shows you what commit was the last to modify each line of any file." -- git blame, with -L to restrict to a line range.
- p. 302 (File Annotation): "If you pass -C to git blame, Git analyzes the file you're annotating and tries to figure out where snippets of code within it originally came from" -- Git does not track renames; it infers moves after the fact.
- p. 302 (Binary Search): "The bisect command does a binary search through your commit history to help you identify as quickly as possible which commit introduced an issue." -- git bisect start, bad, good <commit>.
- p. 303 (Binary Search): "Git figured out that about 12 commits came between the commit you marked as the last good commit (v1.0) and the current bad version" -- each answer halves the range; Git then names the first bad commit.
- p. 303 (Binary Search): "When you're finished, you should run git bisect reset to reset your HEAD to where you were before you started"
- p. 304 (Binary Search): "if you have a script that will exit 0 if the project is good or non-0 if the project is bad, you can fully automate git bisect" -- git bisect start HEAD v1.0, then git bisect run test-error.sh.

### Git Hooks (8.3)
- p. 360 (Git Hooks): "Client-side hooks are triggered by operations such as committing and merging, while server-side hooks run on network operations such as receiving pushed commits."
- p. 360 (Installing a Hook): "any properly named executable scripts will work fine" -- hooks live in .git/hooks; the bundled examples end in .sample and must be renamed.
- p. 361 (Client-Side Hooks): "client-side hooks are not copied when you clone a repository" -- to enforce a policy, do it on the server side.
- p. 361 (Committing-Workflow Hooks): "Exiting non-zero from this hook aborts the commit, although you can bypass it with git commit --no-verify." -- pre-commit inspects the snapshot: tests, lint, trailing whitespace, documentation.
- p. 361 (Committing-Workflow Hooks): "It lets you edit the default message before the commit author sees it." -- prepare-commit-msg, for auto-generated messages (merges, squashes, templates).
- p. 361 (Committing-Workflow Hooks): "If this script exits non-zero, Git aborts the commit process, so you can use it to validate your project state or commit message before allowing a commit to go through." -- commit-msg receives the path of the message file.
- p. 361 (Committing-Workflow Hooks): "Generally, this script is used for notification or something similar." -- post-commit takes no parameters.
- p. 362 (Email Workflow Hooks): "it is run after the patch is applied but before a commit is made, so you can use it to inspect the snapshot before making the commit" -- pre-applypatch under git am; applypatch-msg checks the message; post-applypatch cannot stop the process.
- p. 362 (Other Client Hooks): "You can use this hook to disallow rebasing any commits that have already been pushed." -- pre-rebase; the bundled example makes assumptions that may not fit a workflow.
- p. 362 (Other Client Hooks): "The post-rewrite hook is run by commands that replace commits, such as git commit --amend and git rebase (though not by git filter-branch)."
- p. 362 (Other Client Hooks): "you can use it to set up your working directory properly for your project environment" -- post-checkout; post-merge restores data Git cannot track, such as permissions.
- p. 362 (Other Client Hooks): "You can use it to validate a set of ref updates before a push occurs (a non-zero exit code will abort the push)." -- pre-push; pre-auto-gc can abort automatic garbage collection.
- p. 362 (Server-Side Hooks): "The pre hooks can exit non-zero at any time to reject the push as well as ... print an error message back to the client"
- p. 363 (pre-receive): "It takes a list of references that are being pushed from stdin; if it exits non-zero, none of them are accepted."
- p. 363 (update): "If the update script exits nonzero, only that reference is rejected; other references can still be updated." -- runs once per branch with ref name, old SHA-1, new SHA-1.
- p. 363 (post-receive): "This script can't stop the push process, but the client doesn't disconnect until it has completed" -- used for notifications, CI, ticket updates.
- p. 363 (Server-Side Hooks): "If you're writing a script/hook that others will need to read, prefer the long versions of command-line flags"

### An Example Git-Enforced Policy (8.4)
- p. 363 (An Example Git-Enforced Policy): "You'll build client scripts that help the developer know if their push will be rejected and server scripts that actually enforce the policies."
- p. 364 (Enforcing a Specific Commit-Message Format): "if the string is absent from any of the commits, exit non-zero so the push is rejected" -- each commit must carry a ticket reference of the form ref: 1234; commits are listed with git rev-list oldrev..newrev.
- p. 365 (Enforcing a Specific Commit-Message Format): "Putting that in your update script will reject updates that contain commits that have messages that don't adhere to your rule."
- p. 366 (Enforcing a User-Based ACL System): "see what files are being introduced for all the commits being pushed, and determine whether the user doing the push has access to update all those files" -- an acl file of avail|users|path lines.
- p. 368 (Testing It Out): "Anything your script echoes to stdout will be transferred to the client."
- p. 369 (Testing It Out): "as long as that update script is there and executable, your repository will never have a commit message without your pattern in it, and your users will be sandboxed"
- p. 369 (Client-Side Hooks): "Having their carefully crafted work rejected at the last minute can be extremely frustrating and confusing" -- and they then have to edit their history.
- p. 369 (Client-Side Hooks): "Because hooks aren't transferred with a clone of a project, you must distribute these scripts some other way" -- users copy them into .git/hooks; Git won't set them up automatically.
- p. 371 (Client-Side Hooks): "you must get your file listing from the staging area instead" -- the client pre-commit uses git diff-index --cached --name-only HEAD because the commit is not yet recorded.
- p. 371 (Client-Side Hooks): "it expects you to be running locally as the same user you push as to the remote machine"
- p. 371 (Client-Side Hooks): "Presumably, the server is already configured with receive.denyDeletes and receive.denyNonFastForwards to enforce this policy" -- so the client can only catch accidental rebases of pushed commits.
- p. 372 (Client-Side Hooks): "The main drawback to this approach is that it can be very slow and is often unnecessary" -- the server refuses non-fast-forward pushes unless forced.

### Git Internals (ch. 10)
- p. 420 (Git Internals): "Git is fundamentally a contentaddressable filesystem with a VCS user interface written on top of it."
- p. 420 (Plumbing and Porcelain): "designed to be chained together UNIX-style or called from scripts" -- plumbing commands, as opposed to user-friendly porcelain; meant as building blocks for tools and scripts.
- p. 420 (Plumbing and Porcelain): "If you want to back up or clone your repository, copying this single directory elsewhere gives you nearly everything you need."
- p. 421 (Plumbing and Porcelain): "The objects directory stores all the content for your database, the refs directory stores pointers into commit objects in that data" -- with HEAD (current branch) and index (staging area) these are the core parts.
- p. 421 (Git Objects): "at the core of Git is a simple key-value data store" -- any content inserted returns a unique key for retrieval (git hash-object -w).
- p. 422 (Git Objects): "This is the SHA-1 hash — a checksum of the content you're storing plus a header" -- stored as .git/objects/<first 2 chars>/<remaining 38>.
- p. 423 (Git Objects): "you aren't storing the filename in your system — just the content. This object type is called a blob."
- p. 423 (Tree Objects): "A single tree object contains one or more entries, each of which is the SHA-1 hash of a blob or subtree with its associated mode, type, and filename."
- p. 425 (Tree Objects): "these three modes are the only ones that are valid for files (blobs) in Git" -- 100644 normal, 100755 executable, 120000 symlink.
- p. 427 (Commit Objects): "You will get a different hash value because of different creation time and author data." -- yet any commit can in principle be reproduced exactly given that data.
- p. 427 (Commit Objects): "it specifies the top-level tree for the snapshot of the project at that point; the parent commits if any" -- then author/committer with timestamp, a blank line, the message.
- p. 428 (Commit Objects): "This is essentially what Git does when you run the git add and git commit commands" -- store blobs, update the index, write trees, write commits referencing parents.
- p. 429 (Object Storage): "Git first constructs a header which starts by identifying the type of object" -- type, space, size in bytes, null byte; SHA-1 over header plus content; then zlib-compressed on disk.
- p. 431 (Object Storage): "All Git objects are stored the same way, just with different types" -- commit and tree content are specifically formatted.
- p. 431 (Git References): "You aren't encouraged to directly edit the reference files; instead, Git provides the safer command git update-ref"
- p. 432 (Git References): "That's basically what a branch in Git is: a simple pointer or reference to the head of a line of work."
- p. 432 (The HEAD): "Usually the HEAD file is a symbolic reference to the branch you're currently on." -- it holds a raw SHA-1 only in detached HEAD state.
- p. 433 (The HEAD): "fatal: Refusing to point HEAD outside of refs/" -- git symbolic-ref is the safe way to read or set HEAD.
- p. 433 (Tags): "It's like a branch reference, but it never moves — it always points to the same commit but gives it a friendlier name."
- p. 434 (Tags): "If you create an annotated tag, Git creates a tag object and then writes a reference to point to it rather than directly to the commit." -- a lightweight tag is only a reference that never moves; a tag can point to any object.
- p. 435 (Remotes): "Remote references differ from branches (refs/heads references) mainly in that they're considered read-only." -- bookmarks to the last known state on the server.
- p. 436 (Packfiles): "although you added only a single line to the end of a 400-line file, Git stored that new content as a completely new object" -- two blobs of 22044 and 22054 bytes.
- p. 436 (Packfiles): "Git does this if you have too many loose objects around, if you run the git gc command manually, or if you push to a remote server."
- p. 437 (Packfiles): "Because you never added them to any commits, they're considered dangling and aren't packed up in your new packfile."
- p. 437 (Packfiles): "the objects on disk before you ran the gc command were collectively about 15K in size, the new packfile is only 7K" -- Git stores deltas between similarly named and sized files.
- p. 438 (Packfiles): "the second version of the file is the one that is stored intact, whereas the original version is stored as a delta" -- the earlier version takes 9 bytes in the pack; the database can be repacked at any time.
- p. 438 (The Refspec): "tells Git to update the reference even if it isn't a fast-forward" -- the leading plus in +<src>:<dst>; the default fetch refspec maps refs/heads/* to refs/remotes/origin/*.
- p. 439 (The Refspec): "the master branch pull was rejected because it wasn't listed as a fast-forward reference" -- override with a + in front of the refspec; partial globs work since Git 2.6.0.
- p. 439 (The Refspec): "you can use namespaces (or directories) to accomplish the same with more structure" -- e.g. qa/* for one team's branches.
- p. 440 (Pushing Refspecs): "You cannot use the refspec to fetch from one repository and push to another one."
- p. 440 (Deleting References): "by leaving off the <src> part, this basically says to make the topic branch on the remote nothing, which deletes it" -- also git push origin --delete topic.
- p. 441 (The Dumb Protocol): "It's difficult to secure or make private, so most Git hosts (both cloud-based and on-premises) will refuse to use it." -- a series of HTTP GETs; needs update-server-info as a post-receive hook.
- p. 443 (The Smart Protocol): "it requires a process on the remote end that is intelligent about Git" -- send-pack/receive-pack for upload, fetch-pack/upload-pack for download.
- p. 443 (Uploading Data): "Each chunk starts with a 4-character hex value specifying how long the chunk is (including the 4 bytes of the length itself)." -- 0000 ends a listing.
- p. 444 (Uploading Data): "Git sends a line for each reference you're updating with the line's length, the old SHA-1, the new SHA-1, and the reference that is being updated." -- all zeros mean nothing was there (new ref) or deletion.
- p. 445 (Downloading Data): "to initiate the upload-pack process to begin sending the packfile of the data it needs" -- after want and have lines the server sends a packfile of what is needed.
- p. 446 (Protocols Summary): "if you need more knowledge than this, you'll probably want to take a look at the Git source code" -- the overview leaves out multi_ack and side-band.
- p. 446 (Maintenance): "it removes objects that aren't reachable from any commit and are a few months old" -- gc also gathers loose objects into packfiles and consolidates packfiles.
- p. 446 (Maintenance): "You must have around 7,000 loose objects or more than 50 packfiles for Git to fire up a real gc command." -- limits set by gc.auto and gc.autopacklimit.
- p. 447 (Maintenance): "If you update a reference, Git doesn't edit this file but instead writes a new file to refs/heads." -- gc moves refs into .git/packed-refs; lookup checks refs first, packed-refs as fallback.
- p. 447 (Data Recovery): "this happens because you force-delete a branch that had work on it, and it turns out you wanted the branch after all; or you hard-reset a branch"
- p. 448 (Data Recovery): "As you're working, Git silently records what your HEAD is every time you change it." -- git reflog and git log -g; recover by making a branch at the lost commit.
- p. 448 (Data Recovery): "The reflog is also updated by the git update-ref command, which is another reason to use it instead of just writing the SHA-1 value to your ref files"
- p. 449 (Data Recovery): "If you run it with the --full option, it shows you all objects that aren't pointed to by another object" -- git fsck finds a dangling commit when the reflog (.git/logs/) is gone.
- p. 449 (Removing Objects): "every clone for all time will be forced to download that large file, even if it was removed from the project in the very next commit"
- p. 449 (Removing Objects): "Be warned: this technique is destructive to your commit history." -- unless done right after an import, all contributors must rebase onto the new commits.
- p. 450 (Removing Objects): "clearly, removing the file from the previous commit didn't remove it from your history" -- size-pack 4868 KB after adding and removing a tarball, against about 2K before.
- p. 451 (Removing Objects): "you can identify the big objects by running another plumbing command called git verify-pack and sorting on the third field in the output" -- then git rev-list --objects --all to find the file name.
- p. 451 (Removing Objects): "The reason to do it this way is speed" -- --index-filter with git rm --cached --ignore-unmatch avoids checking out each revision.
- p. 452 (Removing Objects): "your reflog and a new set of refs that Git added when you did the filter-branch under .git/refs/original still do" -- they must be removed before repacking.
- p. 452 (Removing Objects): "The packed repository size is down to 8K, which is much better than 5MB." -- the object stays loose until git prune --expire now.

### Environment Variables (10.8)
- p. 453 (Repository Locations): "If this isn't specified, Git walks up the directory tree until it gets to ~ or /, looking for a .git directory at every step." -- GIT_DIR; GIT_CEILING_DIRECTORIES stops the search earlier.
- p. 453 (Repository Locations): "the current working directory is regarded as the top level of your working tree" -- when GIT_DIR is set but no work tree is.
- p. 454 (Committing): "uses these environment variables as its primary source of information, falling back to configuration values only if these aren't present" -- GIT_AUTHOR_NAME/EMAIL/DATE and GIT_COMMITTER_NAME/EMAIL/DATE.
- p. 454 (Networking): "GIT_SSL_NO_VERIFY tells Git not to verify SSL certificates." -- for self-signed certificates or half-set-up servers.
- p. 455 (Diffing and Merging): "GIT_MERGE_VERBOSITY controls the output for the recursive merge strategy." -- values 0 to 5 and above; default 2.
- p. 455 (Debugging): "Git has a fairly complete set of traces embedded, and all you need to do is turn them on." -- GIT_TRACE, GIT_TRACE_PACK_ACCESS, GIT_TRACE_PACKET.
- p. 456 (Debugging): "The output shows how long each particular git invocation takes." -- GIT_TRACE_PERFORMANCE; the example git gc took 6.11 s in total.
- p. 457 (Miscellaneous): "Note that this isn't the easiest way to customize how ssh is invoked; it won't support extra command-line parameters." -- GIT_SSH; GIT_SSH_COMMAND accepts arguments.
- p. 458 (Miscellaneous): "GIT_REFLOG_ACTION lets you specify the descriptive text written to the reflog."
- p. 458 (Summary): "Understanding how Git works at a lower level should make it easier to understand why it's doing what it's doing and also to write your own tools and helper scripts"

### Appendix A, opening (read as part of the assigned range)
- p. 459 (Graphical Interfaces): "there's nothing these graphical clients can do that the command-line client can't" -- some clients expose a curated subset to support one way of working.
- p. 463 (Installation): "set up sane defaults for many common configuration options, such as credential caches and CRLF behavior" -- the GitHub desktop clients.
- p. 464 (Recommended Workflow): "If this fails because of a merge conflict, fall back to git pull --no-rebase." -- the Sync button runs git pull --rebase, then git push.

## Readings for our work
- Our pre-commit gate (method/check_all.py via method/hooks/pre-commit) can be skipped by any author with git commit --no-verify, and does not exist in a fresh clone until sh method/setup.sh runs. A local hook is therefore a convenience, not enforcement: the same checks must also run where the author cannot skip them (GitHub Actions on push and pull request, with branch protection requiring them). Check: push a commit made with --no-verify to a test branch and confirm CI fails it. Rests on: p. 361 (--no-verify; hooks not copied on clone), p. 369 (hooks must be distributed some other way), p. 363 (pre-receive/update reject on the server). Would not apply if: the repository already runs check_all.py in required CI, or nobody but the gate's author ever commits.
- The commit-msg rule (Serves: P.. / Method: ..) matches the book's ticket-reference policy, which it enforces twice: a client commit-msg hook for early feedback and a server update hook that inspects every pushed commit with git rev-list oldrev..newrev. We should check the trailer on every commit in a pushed range, not only HEAD, so that a squashed or rebased range cannot carry one unlabeled commit. Check: a CI step that loops over git rev-list base..head and fails on any commit lacking the trailer. Rests on: p. 364-365 (rev-list over the pushed range, exit non-zero), p. 369 (rejection at push is frustrating, hence client hooks too). Would not apply if: all work lands only as single squash-merges whose final message is itself checked.
- A check written by the same hand it checks is weakest where it runs on the client: the book's client pre-commit even assumes the local user equals the pushing user. Server-side or CI enforcement with its own copy of the rules (not read from the working tree under change) is the independent layer. Rests on: p. 371 (client script assumes same user; rules read from .git/acl), p. 369 (server script makes the policy hold as long as it is there and executable). Would not apply if: the rules file the CI reads is itself editable in the same commit without review; then the check needs a protected copy.
- For the DLL patches to the GitLab repository, a line-ending rewrite looks to Git like every line removed and re-added, and -Xignore-space-change can leave a file with mixed line endings. Before sending a patch or merge request, inspect it with git diff --stat and compare to git diff -b (or --ignore-cr-at-eol): any file whose line count changes a lot between the two contains a whitespace or CRLF rewrite and must be redone, not merged with whitespace options. Rests on: p. 278 (DOS line-ending change touches every line), p. 280 (sign of a whitespace conflict), p. 282 (ignore-space-change leaves mixed endings; fixing before merge is better). Would not apply if: the GitLab repository normalises line endings on its side (e.g. a .gitattributes eol rule) so that CRLF differences never reach the diff.
- Commits that mix several concerns can be split locally before pushing with rebase -i (edit, reset HEAD^, stage in parts, continue), but only while unpushed; after a push the remedy is a new commit, not rewriting. Rests on: p. 249 (pushed work is final), p. 254-255 (splitting changes later SHA-1s). Would not apply if: the branch is private and nobody, including CI caches or the patch recipients, has fetched it.
- Keeping our patch branch rebased on the moving GitLab upstream will repeat the same conflicts each time; enabling rerere (git config rerere.enabled true) records each resolution once. Check: the second rebase onto upstream reports Resolved ... using previous resolution. Each auto-resolution should still be reviewed with git diff before continuing, since rerere replays by hunk content. Rests on: p. 294-295 (rerere purpose and the rebase use case), p. 299 (replayed resolution). Would not apply if: patches are delivered once and never rebased.
- When a harness metric or a DLL build regresses between two known commits, git bisect run with a script that exits 0 for good and non-zero for bad finds the first bad commit without manual steps; the script must be deterministic (fixed seed) or its exit code will mislead the search. This answers which commit, not why. Rests on: p. 302-304 (bisect, automated with exit codes). Would not apply if: the regression only appears statistically across many seeds, where one run per commit cannot classify it; then each bisect step needs the full seeded comparison or a formula.
- The prediction register (method/mission/register.json, append-only) can be verified from Git itself rather than trusted: every committed version of the file is a content-addressed blob, so a check can walk git log -p over that path and fail if any line ever disappears or changes. This is a tool to build only if the current ledger check does not already do it. Rests on: p. 421-423 (content-addressed blobs), p. 428 (commits reference trees and parents). Would not apply if: the history is rewritten (filter-branch, force-push), which is exactly what server-side non-fast-forward refusal must prevent (p. 371).
- Generated files edited by hand can be caught by regenerating them and comparing hashes: the same bytes always give the same blob SHA-1 (git hash-object), so a check can render each .md.in and compare git hash-object of the output with the committed blob. Rests on: p. 422 (SHA-1 of header plus content), p. 429-431 (object format). Would not apply if: rendering is not byte-deterministic (timestamps, ordering), which would first have to be fixed.
- Game saves, logs and DuckDB files committed to the repository stay in every clone forever even after deletion, and removing them needs a destructive history rewrite. Keep such data out of the repository (or in a separate store), and check with git rev-list --objects --all plus git verify-pack sorting for large blobs. Rests on: p. 449-452 (large file stays in history; removal is destructive; refs/original and reflog hold it). Would not apply if: the data files are small text whose history we want versioned anyway.
- Lost local work after a mistaken reset --hard or branch deletion is usually recoverable through git reflog or git fsck --full, but uncommitted changes overwritten by reset --hard are not. So commit or stash before any reset --hard, merge or checkout with paths. Rests on: p. 269 (only --hard destroys data), p. 277 (checkout with paths not WD safe), p. 448-449 (reflog, fsck). Would not apply if: the work was never written to a commit or stash.
- For a reproducible experiment record, a commit's hash depends on author and committer dates, so the same tree committed twice gives different SHA-1s; identify experiment inputs by tree or blob hash (git rev-parse HEAD^{tree}) rather than commit hash when comparing runs across rebases. Rests on: p. 427 (hash differs by creation time and author data), p. 454 (GIT_AUTHOR_DATE and GIT_COMMITTER_DATE override). Would not apply if: commits are never rebased or amended after a run is recorded.
- GIT_TRACE_PERFORMANCE and GIT_TRACE show where time goes inside hooks and plumbing calls; if the pre-commit gate is slow, measure it this way before adding or removing checks. Rests on: p. 455-456 (trace variables). Would not apply if: the time is spent in our Python checks rather than in Git, which a plain timer on check_all.py shows.
