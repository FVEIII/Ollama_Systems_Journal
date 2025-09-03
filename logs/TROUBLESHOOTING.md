## 🛠 Markdown & GitHub Troubleshooting Checklist

This checklist helps diagnose and fix common issues with Markdown rendering in VS Code and GitHub.

---

### **1. Code Blocks Not Rendering Correctly**
- **Symptom:** Content appears as plain text or smushed into one paragraph on GitHub.
- **Fix:**
  - Make sure code is wrapped in triple backticks:
    ```
    ```markdown
    # Example Heading
    ```
    ```
  - GitHub requires *fencing* for Markdown to keep formatting intact.

---

### **2. Tree Diagrams Render Incorrectly**
- **Symptom:** Repository structure tree collapses into a single line or loses indentation.
- **Fix:**
  - Use `text` or `plaintext` as the language hint in the code block:
    ```
    ```text
    ├── folder/
    │   └── file.txt
    └── README.md
    ```
    ```

---

### **3. Copy/Paste Issues Between ChatGPT and VS Code**
- **Symptom:** Markdown looks correct in ChatGPT but breaks when pasted into VS Code.
- **Causes:**
  - ChatGPT rendered the text instead of showing raw characters.
  - Hidden characters like backticks were stripped during copy.
- **Fix:**
  - Always copy from **inside a code block**.
  - Verify in VS Code by switching to **Preview Mode** (`Ctrl + Shift + V`).

---

### **4. GitHub Preview Differs from VS Code**
- **Symptom:** Markdown looks fine locally but appears broken on GitHub.
- **Fix:**
  - Commit and push changes, then view directly on GitHub.
  - Confirm the file extension is `.md`.
  - Look for extra spaces, tabs, or hidden characters:
    - Use `View → Render Whitespace` in VS Code.

---

### **5. Confirm Formatting with a Small Test**
If problems persist, make a small test file:

# Test Heading
- Bullet 1
- Bullet 2

- Push to GitHub and check the rendered result.
- If the test file works, the issue is within your original file formatting.

---

### **6. Quick Commands**
- **Preview Markdown in VS Code:**  
  `Ctrl + Shift + V`  
- **Open Side-by-Side Markdown Preview:**  
  `Ctrl + K, V`

---

### **7. Workflow Tip**
When asking for Markdown help:
1. Share a screenshot of:
   - VS Code editor
   - GitHub rendered view
2. Mention if backticks are visible in the source.
3. Confirm if you're pasting into a `.md` file.

---

### **Summary**
Most Markdown rendering issues come from **missing or invisible backticks**.  
Always use explicit fenced code blocks and verify how it looks in both **VS Code Preview** and **GitHub** before finalizing.
