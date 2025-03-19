## GitHub Deployment

// ... existing deployment content ...

## Working with Development Branch

1. **Create and Switch to Development Branch**:
   ```bash
   # Create and switch to development branch
   git checkout -b development

   # Or if you want to create from main branch
   git checkout main
   git checkout -b development
   ```

2. **Push Development Branch to GitHub**:
   ```bash
   # Push the development branch to GitHub
   git push -u origin development
   ```

3. **Workflow for Development**:
   ```bash
   # Make sure you're on development branch
   git checkout development

   # Create feature branch for new feature
   git checkout -b feature/your-feature-name

   # Make changes and commit
   git add .
   git commit -m "Add new feature"

   # Push feature branch
   git push -u origin feature/your-feature-name

   # After feature is complete, merge back to development
   git checkout development
   git merge feature/your-feature-name
   git push origin development
   ```

4. **Branch Protection Rules** (Recommended):
   - Go to repository Settings → Branches
   - Add branch protection rule for 'development'
   - Enable:
     - Require pull request reviews
     - Require status checks to pass
     - Require branches to be up to date
     - Include administrators

5. **Pull Request Process**:
   - Create pull request from feature branch to development
   - Add description of changes
   - Request reviews from team members
   - Address review comments
   - Merge after approval

6. **Keeping Development Branch Updated**:
   ```bash
   # Update development branch with main
   git checkout development
   git fetch origin
   git merge origin/main

   # Update your feature branch
   git checkout feature/your-feature-name
   git merge development
   ```

7. **Common Branch Commands**:
   ```bash
   # List all branches
   git branch -a

   # Switch branches
   git checkout branch-name

   # Create and switch to new branch
   git checkout -b new-branch-name

   # Delete local branch
   git branch -d branch-name

   # Delete remote branch
   git push origin --delete branch-name
   ```

## API Documentation

// ... rest of the existing content ... 