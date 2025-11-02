# Web Interface Guide

Beautiful, user-friendly web interface for the Multi-Agent Research Assistant.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` - Web framework
- `plotly` - Interactive charts
- `anthropic` - Claude API
- `python-dotenv` - Environment variables

### 2. Launch the Web Interface

```bash
cd "C:\Users\harry\OneDrive\Desktop\Research Assistant"
streamlit run app.py
```

The interface will automatically open in your browser at `http://localhost:8501`

**Alternative:** Use Python directly:
```bash
python -m streamlit run app.py
```

### 3. Share with Colleagues

**Option A: Local Network Sharing**
When you run streamlit, you'll see:
```
Network URL: http://192.168.1.X:8501
```
Share this URL with colleagues on the same network!

**Option B: Cloud Deployment** (See deployment section below)

---

## Interface Overview

### 🎯 Four Main Modes

#### 1. 📝 Analysis Mode
**Purpose:** Run multi-agent analysis on marketing materials

**How to Use:**
1. Choose input method (Paste Text or Upload File)
2. Enter your marketing document
3. Add optional context (target audience, price point, etc.)
4. Click "🚀 Run Analysis"
5. View results organized by agent
6. Download results as JSON

**Features:**
- Real-time analysis
- Organized agent insights
- Executive summary generation
- Downloadable results
- Execution metrics

#### 2. 🧪 A/B Testing Mode
**Purpose:** Compare different prompt variants scientifically

**How to Use:**
1. Select agent to test (Strategic Analyst or Audience Evaluator)
2. Set number of iterations (3-5 recommended)
3. Provide test document (or use from Analysis mode)
4. Click "🧪 Run A/B Test"
5. View performance comparison
6. Download detailed results

**Features:**
- Side-by-side variant comparison
- Interactive radar charts
- Performance metrics visualization
- Statistical rankings
- Winner identification

#### 3. 📊 Results History
**Purpose:** Browse and review past analyses and tests

**How to Use:**
1. Select result type (Analyses or A/B Tests)
2. Choose from list of past results
3. View detailed breakdown
4. Download for further analysis

**Features:**
- Chronological listing
- Quick preview
- Full result display
- Export capabilities

#### 4. ⚙️ Configuration
**Purpose:** Manage prompt variants and settings

**How to Use:**
1. Select agent to configure
2. View existing variants
3. Add new variants with custom prompts
4. Export/import configurations

**Features:**
- Visual variant editor
- Temperature controls
- Hypothesis documentation
- Configuration backup/restore

---

## Visual Guide

### Dashboard Layout

```
┌─────────────────────────────────────────────────────────┐
│  🤖 Multi-Agent Research Assistant                      │
├──────────────┬──────────────────────────────────────────┤
│              │                                          │
│  📝 Sidebar  │         Main Content Area               │
│              │                                          │
│  • Navigation│  • Input forms                          │
│  • API Status│  • Action buttons                       │
│  • Quick Stats│  • Results display                      │
│  • Help      │  • Visualizations                       │
│              │                                          │
└──────────────┴──────────────────────────────────────────┘
```

### Analysis Workflow

```
Input Document → Select Context → Run Analysis → View Results
     ↓              ↓                 ↓              ↓
  [Text Area]  [Optional Box]   [Progress Bar]  [Tabbed View]
```

### A/B Test Workflow

```
Choose Agent → Set Iterations → Run Test → Compare Variants
     ↓              ↓              ↓            ↓
 [Dropdown]   [Number Input]  [Progress]   [Charts & Rankings]
```

---

## Key Features

### 🎨 Beautiful Visualizations

**Radar Charts** - Compare all metrics simultaneously
- Consistency
- Specificity
- Actionability
- Technical Density
- Speed

**Bar Charts** - Detailed metric-by-metric comparison

**Performance Graphs** - Execution time and success rates

### 📊 Real-Time Metrics

**Live Status Indicators:**
- API connection status
- Analysis count
- Test count
- Execution progress

**Performance Tracking:**
- Token usage
- Execution time
- Success rates
- Model information

### 💾 Data Management

**Automatic Saving:**
- All analyses saved to `outputs/`
- All tests saved to `outputs/tests/`
- Timestamped filenames

**Export Options:**
- JSON (full data)
- TXT (readable reports)
- Configuration backups

### 🎯 User-Friendly Design

**No Command Line Required** - Point-and-click interface

**Responsive Layout** - Works on different screen sizes

**Color-Coded Results:**
- 🟢 Green = Success
- 🟡 Yellow = Warning
- 🔴 Red = Error

**Progress Indicators** - Clear feedback during processing

---

## Tips & Best Practices

### 📝 For Analysis Mode

1. **Add Context** - More context = better analysis
   ```
   Good: "Target: Women 45-60, Premium skincare, $450 price point"
   Basic: "Skincare product"
   ```

2. **Document Length** - 100-500 words is optimal

3. **Use Upload** - For longer documents or repeated testing

4. **Save Results** - Download important analyses for later reference

### 🧪 For A/B Testing

1. **Iterations** - 3-5 iterations for reliable results

2. **Test Documents** - Use representative examples

3. **Compare Fairly** - Use same document across all tests

4. **Document Hypotheses** - Note why you expect certain variants to perform better

### ⚙️ For Configuration

1. **Backup First** - Export config before major changes

2. **Test Incrementally** - Add one variant at a time

3. **Document Changes** - Use clear hypotheses and expected performance descriptions

4. **Temperature Settings:**
   - `0.2` = More focused, consistent
   - `0.3-0.4` = Balanced (recommended)
   - `0.5+` = More creative, variable

---

## Troubleshooting

### "API Key Missing" Error

**Solution:**
1. Create `.env` file in project root
2. Add: `ANTHROPIC_API_KEY=your_key_here`
3. Restart streamlit

### "Port Already in Use"

**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Slow Performance

**Solutions:**
- Reduce iterations in A/B tests
- Use temperature 0.2-0.3 (faster)
- Close unused browser tabs
- Check internet connection

### Can't Access from Another Computer

**Solution:**
```bash
streamlit run app.py --server.address 0.0.0.0
```

### Results Not Appearing

**Solutions:**
1. Check `outputs/` folder exists
2. Verify API key is working
3. Look for error messages in terminal
4. Refresh browser (Ctrl+R)

---

## Keyboard Shortcuts

- `Ctrl+R` - Refresh page
- `Ctrl+K` - Focus sidebar
- `Ctrl+/` - Toggle theme (light/dark)
- `Esc` - Close modals/expanders

---

## Sharing with Colleagues

### Method 1: Local Network (Easiest)

1. Start the app:
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```

2. Find your IP address:
   - Windows: `ipconfig` (look for IPv4)
   - Mac/Linux: `ifconfig` (look for inet)

3. Share URL with colleagues:
   ```
   http://YOUR_IP_ADDRESS:8501
   ```

**Example:** `http://192.168.1.45:8501`

### Method 2: Streamlit Cloud (Public Access)

1. Create GitHub repository
2. Push your code
3. Go to [share.streamlit.io](https://share.streamlit.io)
4. Deploy from GitHub
5. Share public URL

**Note:** Add API key as a secret in Streamlit Cloud settings!

### Method 3: Docker Container (Advanced)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

Build and run:
```bash
docker build -t research-assistant .
docker run -p 8501:8501 research-assistant
```

---

## Advanced Configuration

### Custom Port

```bash
streamlit run app.py --server.port 9000
```

### Custom Theme

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Performance Tuning

In `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200

[browser]
gatherUsageStats = false
```

---

## Security Considerations

### ⚠️ Important

1. **API Keys** - Never commit `.env` to version control
2. **Network Access** - Only share on trusted networks
3. **Input Validation** - App validates all inputs
4. **File Uploads** - Limited to .txt and .md files

### Best Practices

- Use environment variables for secrets
- Restrict network access if deploying publicly
- Regularly update dependencies
- Monitor API usage
- Back up important configurations

---

## Updating the Interface

### Pull Latest Changes

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Add Custom Features

Edit `app.py` and add new sections:

```python
elif page == "🆕 My New Feature":
    st.header("🆕 My New Feature")
    # Your custom code here
```

### Modify Visualizations

Change charts in A/B Testing section:

```python
fig = px.bar(...)  # Modify chart type and parameters
st.plotly_chart(fig, use_container_width=True)
```

---

## Support Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Plotly Charts**: https://plotly.com/python
- **Claude API**: https://docs.anthropic.com

## Next Steps

1. ✅ Launch the interface: `streamlit run app.py`
2. 📝 Run your first analysis
3. 🧪 Test some prompt variants
4. 👥 Share with your team
5. ⚙️ Customize to your needs

---

**Enjoy your new web interface!** 🎉
