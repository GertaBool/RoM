# The Git project, gitworkflows(7): An overview of recommended workflows with Git (Git manual page, Git documentation)
Source: lit3/gitworkflows/doc.txt. Read: lines 1-475 (all).

## What it says
- DESCRIPTION: "This document attempts to write down and motivate some of the workflow elements used for `git.git` itself." -- the page describes the Git project's own workflow.
- DESCRIPTION: "Many ideas apply in general, though the full workflow is rarely required for smaller projects with fewer people involved." -- stated limit of scope.
- DESCRIPTION: "Do not always take them literally; you should value good reasons for your actions higher than manpages such as this one." -- the rules are guidance, not law.
- SEPARATE CHANGES: "you should try to split your changes into small logical steps, and commit each of them." -- one logical step per commit.
- SEPARATE CHANGES: "They should be consistent, working independently of any later commits, pass the test suite, etc." -- each commit must stand on its own and pass the tests.
- SEPARATE CHANGES: "This makes the review process much easier, and the history much more useful for later inspection and analysis" -- the stated reasons, naming git-blame and git-bisect as the tools that benefit.
- SEPARATE CHANGES: "try to split your work into small steps from the very beginning." -- split at the start, not afterwards.
- SEPARATE CHANGES: "It is always easier to squash a few commits together than to split one big commit into several." -- asymmetry between squashing and splitting.
- SEPARATE CHANGES: "You can always go back later and edit the commits with `git rebase --interactive` before you publish them." -- history may be cleaned up before publication.
- SEPARATE CHANGES: "You can use `git stash push --keep-index` to run the test suite independent of other uncommitted changes" -- test exactly what is being committed, not the working tree.
- MANAGING BRANCHES: "Merges have many advantages, so we try to solve as many problems as possible with merges alone." -- merge preferred over cherry-pick.
- MANAGING BRANCHES: "merging works at the branch level, while cherry-picking works at the commit level." -- and so merges scale to many commits and contributors.
- MANAGING BRANCHES: "a merge commit is a" promise "that all changes from all its parents are now included." -- (word promise quoted in source) a merge is easier to understand for this reason.
- MANAGING BRANCHES: "There is a tradeoff of course: merges require a more careful branch management." -- the cost of the merge approach.
- Graduation: "As a given feature goes from experimental to stable, it also" graduates "between the corresponding branches of the software." -- features move between integration branches maint, master, next and seen.
- Graduation: "'next' is intended as a testing branch for topics being tested for stability for master." -- next is the test stage before master.
- Graduation: "'seen' (patches seen by the maintainer) is an integration branch for things that are not quite ready for inclusion yet" -- a fourth branch used differently.
- Graduation: "the feature enters at an unstable branch (usually 'next' or 'seen'), and" graduates "to 'master' for the next release once it is considered stable enough." -- the path of a feature.
- Merging upwards (Rule): "Always commit your fixes to the oldest supported branch that requires them." -- then merge the integration branches upwards periodically.
- Merging upwards: "This gives a very controlled flow of fixes." -- a fix applied to master that is also needed on maint has to be cherry-picked downwards; occasional cases are "nothing to worry about unless you do it very frequently."
- Topic branches: "Committing everything directly on the integration branches leads to many problems" -- bad commits must be reverted one by one; parallel work "mixes up the changes, creating further confusion."
- Topic branches (Rule): "Make a side branch for every topic (feature, bugfix, ...). Fork it off at the oldest integration branch that you will eventually want to merge it into." -- one branch per topic.
- Topic branches: "you can first merge a bugfix to 'next', give it some testing time, and merge to 'maint' when you know it is stable." -- testing on an unstable branch before the stable one.
- Topic branches: "a topic that has been merged elsewhere should not be rebased." -- rebasing clashes with merging once the topic is shared.
- Topic branches: "merging an integration branch into your topics -- and by extension, merging anything upstream into anything downstream on a regular basis -- is frowned upon" -- no habitual merges.
- Topic branches (Rule): "Do not merge to downstream except with a good reason: upstream API changes affect your branch; your branch no longer merges to upstream cleanly; etc." -- the allowed reasons.
- Topic branches: "Otherwise, the topic that was merged to suddenly contains more than a single (well-separated) change." -- and the many small merges "will greatly clutter up history."
- Throw-away integration: "we want to avoid merging them anywhere" stable "because such merges cannot easily be undone." -- the problem of testing topics together.
- Throw-away integration (Rule): "To test the interaction of several topics, merge them into a throw-away branch. You must never base any work on such a branch!" -- integration testing on a disposable branch.
- Throw-away integration: "If you make it (very) clear that this branch is going to be deleted right after the testing, you can even publish this branch" -- seen is Git's official throw-away branch.
- Branch management for a release: "The 'master' branch is supposed to be a superset of 'maint'." -- otherwise maint fixes miss the feature release.
- Branch management for a release (Recipe): "This command should not list any commits." -- the check is git log master..maint; if it lists commits, merge maint into master.
- Branch management for a release: "The push could also trigger a post-update hook to perform release-related items such as building release tarballs" -- release work automated by a hook.
- Maintenance branch management: "The 'maint' branch should now be fast-forwarded to the newly released code" -- with git merge --ff-only master; failure means some maint fixes were missed.
- Branch management for next and seen: "the integration branch 'next' may optionally be rewound and rebuilt from the tip of 'master' using the surviving topics on 'next'" -- after a feature release.
- Branch management for next and seen: "the topic is reverted out of 'next' but the fact remains in the history that it was once merged and reverted." -- rebuilding gives such topics a clean slate.
- Branch management for next and seen: "you should make a public announcement indicating that 'next' was rewound and rebuilt." -- not needed for seen, being throw-away.
- DISTRIBUTED WORKFLOWS: "the merge workflow can propagate full history, including merges, while patches cannot." -- the two workflows, merge and patch; in git.git only subsystem maintainers merge.
- DISTRIBUTED WORKFLOWS: "the maintainer(s) may impose restrictions, such as" Signed-off-by "requirements, that all commits/patches submitted for inclusion must adhere to." -- consult the project's documentation.
- Merge workflow: "Do 'not' use 'git pull' unless you actually want to merge the remote branch." -- pull is fetch plus merge.
- Merge workflow: "they can ask downstream to do the merge and resolve the conflicts themselves (perhaps they will know better how to resolve them)." -- the rare case where downstream should merge from upstream.
- Patch workflow: "use linkgit:git-format-patch[1] to generate the corresponding emails (highly recommended over manually formatting them because it makes the maintainer's life easier)." -- generated, not hand-made patches.
- Patch workflow: "you will have to rebase your topic (you cannot use a merge because you cannot format-patch merges)" -- when a patch no longer applies to upstream.
- Patch workflow: "Presumably you have not published your topic other than by mail, so rebasing it is not a problem." -- rebase is safe on unpublished topics.
- Patch workflow: "`git am -3` will use index information contained in patches to figure out the merge base." -- three-way merge helps when importing patches with conflicts.

## Readings for our work
- Inference: each commit in the research repository and each patch to the DLL should hold one logical step that passes the checks on its own (the history of commits mixing several concerns is the failure this rules out). Check: for every commit, `git show --stat` touches one concern, and `method/check_all.py` passes when run on that commit alone (e.g. in a `git rebase -x` pass). Rests on: SEPARATE CHANGES bullets. Would not apply if: a change cannot be split without leaving an intermediate commit that fails the checks; then it is one step.
- Inference: run the pre-commit checks against the staged content only (stash with --keep-index or check the index), so that uncommitted files cannot make a commit pass or fail. Rests on: the git stash push --keep-index point. Would not apply if: the gate already reads the index rather than the working tree.
- Inference: keep each DLL change for the GitLab repository on its own topic branch forked from the oldest branch it must reach, and test combinations of topics on a throw-away integration branch that nothing is based on. Rests on: Topic branches rule; Throw-away integration rule. Would not apply if: the upstream GitLab project accepts only one branch or a single maintainer works there alone with no parallel topics.
- Inference: do not merge upstream into a topic branch habitually; merge only when an upstream change affects the topic or it no longer merges cleanly, so each merge request stays a single change. Rests on: the Merge to downstream rule and its stated reasons. Would not apply if: the upstream requires branches to be kept up to date before review.
- Inference: produce patches for the GitLab repository with git format-patch (or a merge request from a branch) rather than by hand, and rebase rather than merge when a patch no longer applies. Rests on: Patch workflow bullets. Would not apply if: delivery is by pushing a branch that the maintainer merges as is.
- Inference: a containment check like git log master..maint (which must print nothing) is a cheap, mechanical test that one branch holds all fixes of another; use the same shape for checking that the delivered patch branch contains every committed fix. Rests on: Branch management for a release recipe. Would not apply if: fixes are delivered by cherry-pick, which this test does not detect (different commit ids).
- Inference: the page's own caveat limits it: the full graduation scheme is for many contributors; for a one-person research repository, topic branches and separate commits apply, the four integration branches do not. Rests on: DESCRIPTION bullets. Would not apply if: several agents or people work on the repository in parallel.
