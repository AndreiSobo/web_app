git push -u origin <branch>		-> publish branch
git pull origin master 			-> sync latest changes
git checkout master
git pull origin master
git checkout -b KAN-3-implement-new-feature

# Git & Jira Workflow: Feature Branches, Pull Requests, and Cleanup

## 1. Start Work on a Jira Ticket

- Find the Jira ticket key (e.g., `KAN-3`).
- Always start from the latest `master` branch:

```bash
git checkout master
git pull origin master
```

## 2. Create a Feature Branch (Jira-Linked)

- Use the Jira key in the branch name for automatic linking:

```bash
git checkout -b KAN-3-implement-new-feature
# You are now automatically switched to the new branch!
```

## 3. Do Your Work

- Make your code changes, commits, etc.
- Use the Jira key in your commit messages:

```bash
git commit -m "KAN-3: Implement new feature"
```

## 4. Publish Your Branch to GitHub

```bash
git push -u origin KAN-3-implement-new-feature
# The -u flag sets up tracking for future pushes
```

## 5. Create a Pull Request (PR)

- Go to GitHub and click "Compare & pull request" or use the link provided after pushing.
- Use the Jira key in the PR title (e.g., `KAN-3: Implement new feature`).
- Add a clear description.
- (Optional) Request a Copilot or team review.


## 6. Review and Merge the Pull Request

- If your team requires code review, you need someone else to approve your PR before merging.
- On the GitHub PR page:
	1. Click the **"Reviewers"** panel (right side of the PR page).
	2. Search for and select the teammate(s) you want to review your code.
	3. Optionally, add a comment or tag them in the PR description (e.g., `@username please review`).
- The reviewer will get a notification and can:
	- Leave comments or request changes
	- Approve the PR if everything looks good
- Once the PR is **approved** (you'll see an "Approved" badge), you or the reviewer can click **"Merge pull request"**.
- This will merge your feature branch into `master`.

## 7. Clean Up: Delete the Feature Branch

- Delete the branch on GitHub (GitHub will prompt you after merging).
- Delete the branch locally:

```bash
git checkout master
git pull origin master  # Make sure master is up to date
git branch -d KAN-3-implement-new-feature
# Use -d (safe delete) or -D (force delete if needed)
```

## 8. Jira Status

- Check your Jira ticket:
	- Some setups auto-move the ticket to "Done" after merge.
	- If not, move it manually to "Done" or the next status.

---

### Summary Table
| Step | Command | Purpose |
|------|---------|---------|
| 1 | `git checkout master`<br>`git pull origin master` | Start from latest master |
| 2 | `git checkout -b KAN-3-implement-new-feature` | Create & switch to feature branch |
| 3 | `git commit -m "KAN-3: ..."` | Commit with Jira key |
| 4 | `git push -u origin ...` | Publish branch to GitHub |
| 5 | PR on GitHub | Link code to Jira ticket |
| 6 | Merge PR | Integrate changes to master |
| 7 | `git branch -d ...` | Delete local branch |
| 8 | Update Jira | Move ticket to Done |

---

**Tip:** Always use the Jira key in branch names, commit messages, and PR titles for best integration!