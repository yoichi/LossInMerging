# Prevent code loss in merging

There are some situations where SCM assisted merging
to the production branch may cause code loss, and developers
should take care of them.

## Typical example

Let's see a simple example of a code loss in merging.
We use git as a SCM and use a small python program to
illustrate a typical case.
At first, clone sample repository as follows.
```
% git clone https://github.com/yoichi/LossInMerging.git
% cd LossInMerging
```

The 'development' branch has 3 commits. The 'production' branch
forked from the first commit (0), and the commit (2)
is already merged.
```
% git log --oneline development
de139f3 ignore whitespaces   ... (2)
f6eac1a define equals method ... (1)
bea0b66 define String class  ... (0)
% git log --oneline production
cc779ca ignore whitespaces   ... (2')
bea0b66 define String class  ... (0)
```

Suppose that we are going to merge the
feature introduced in (1) to the 'production'
branch.
Switch to the 'production' branch and
cherry-pick the commit (1) from 'development'.
```
% git checkout production
Switched to branch 'production'
% git cherry-pick f6eac1a
[production 56efba1] define equals method
1 file changed, 2 insertions(+)
% git log --oneline
56efba1 define equals method
cc779ca ignore whitespaces
bea0b66 define String class
```

There is no conflict and everything seems fine.
But the merged code in 'production' has a lost part
compared to 'development'.

```
% git diff production development
diff --git a/string.py b/string.py
index 326c9d7..034715d 100644
--- a/string.py
+++ b/string.py
@@ -4,4 +4,4 @@ class String:
     def get(self):
         return self.__data
     def equals(self, other):
-        return self.__data == other
+        return self.__data == other.replace(" ", "")
```

Probably, this difference is unexpected. It may cause
some problem on pre-release evaluation environment, or
on user environments if it is not detected in the evaluation process.

## Countermeasures

Compare the commits in each branch carefully, you will find
the order of commits is different between them.
```
% git log --oneline development
de139f3 ignore whitespaces   ... (2)
f6eac1a define equals method ... (1)
bea0b66 define String class  ... (0)
% git log --oneline production
56efba1 define equals method ... (1')
cc779ca ignore whitespaces   ... (2')
bea0b66 define String class  ... (0)
```

In fact there was a conflict in the merge for the commit (2'),
and it was resolved by excluding the unrelated part in terms of
the change (2). Since the SCM doesn't know the relation between
the code thrown away in (2') and the additional work needed in
merge (1'), the loss must be prevented by developers.

First, we should **investigate the cause of the conflict**
at the first conflict in (1'). Then, we should consider
how can we prevent the conflict, or
how can we prevent code loss in the future.
There are several candidate of countermeasures e.g.
* keep the order of commits
* guard by test cases
* record the unfinished works for future merge

and the suitable solution depends on the situation.

## keep the order of commits

After some investigation, we find the cause of the conflict at (2') is
that the dependent change (1) is not merged yet.
A solution to avoid the conflict is merging (1) before (2).
If the order of commits is preserved in merging, the conflict
shown in the example disappears.
As noted previously, whether the solution is acceptable depends
on the situation. If we should not merge (1) in production line,
or if there is some inevitable reason to merge (2) before (1),
we cannot adopt this plan.

## guard by test cases

We might have test codes to detect regression caused by code changes
_as illustrated in another development branch 'withtest' in the example
repository_. The test code may conflict at (1'), _as illustrated in branch 'production_withtest'_,
then we have a chance to know the possibility of the code loss.
Here, we should note that we might overlook the possibility of the code loss at the conflict.
We might resolve the conflict without recovering the test for composite case along
with the lost production code. Don't miss the cause of the
second conflict.

## record the unfinished works for future merge

We might use some issue tracking system (e.g. GitHub issues, Redmine, etc)
cooperate with the SCM. If we store a note on the issue for (1)
at the first conflict on merging (2'), then we have a chance to know the contents of the
unfinished works on merging (1) in the future.

# Summary

Don't miss the cause of the conflict.
