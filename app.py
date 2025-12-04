import streamlit as st
import re
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

# Expected HTML code
EXPECTED_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Advanced Bootstrap Grid Layout</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    /* Custom media query (extra challenge) */
    @media (max-width: 600px) {
      .hero-text {
        font-size: 1.2rem;
        text-align: center;
      }
    }
    .box {
      padding: 20px;
      color: white;
      border-radius: 8px;
    }
  </style>
</head>
<body>
  <div class="container mt-4">
    <!-- Hero Section -->
    <div class="row mb-4">
      <div class="col-12 bg-dark text-white p-4 hero-text">
        <h2 class="mb-0">Advanced Bootstrap Grid Layout</h2>
        <p class="mb-0">This layout changes at 3 different breakpoints.</p>
      </div>
    </div>
    <!-- Main 3-Column Layout -->
    <div class="row g-3">
      <div class="col-12 col-md-6 col-lg-4">
        <div class="box bg-primary">Main Box 1</div>
      </div>
      <div class="col-12 col-md-6 col-lg-4">
        <div class="box bg-success">Main Box 2</div>
      </div>
      <div class="col-12 col-md-12 col-lg-4">
        <div class="box bg-danger">Main Box 3</div>
      </div>
    </div>
    <!-- Nested Grid Section -->
    <div class="row mt-4">
      <div class="col-12 col-lg-8">
        <div class="box bg-warning text-dark">
          <h4>Main Content Area</h4>
          <!-- Nested Row -->
          <div class="row mt-3">
            <div class="col-6 col-md-4">
              <div class="box bg-secondary">Nested 1</div>
            </div>
            <div class="col-6 col-md-4">
              <div class="box bg-info text-dark">Nested 2</div>
            </div>
            <div class="col-12 col-md-4">
              <div class="box bg-dark">Nested 3</div>
            </div>
          </div>
        </div>
      </div>
      <!-- Sidebar -->
      <div class="col-12 col-lg-4">
        <div class="box bg-primary">Sidebar Area</div>
      </div>
    </div>
  </div>
  <!-- Bootstrap JS -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

def calculate_similarity(text1, text2):
    """Calculate similarity between two texts"""
    return SequenceMatcher(None, text1.strip(), text2.strip()).ratio()

def check_ai_indicators(code):
    """Check for common AI-written code indicators"""
    ai_score = 0
    indicators = []
    
    # Check for perfect formatting
    if re.search(r'^\s{2}', code, re.MULTILINE):
        ai_score += 1
        indicators.append("Consistent 2-space indentation")
    
    # Check for comments
    comment_count = len(re.findall(r'<!--.*?-->', code, re.DOTALL))
    if comment_count >= 3:
        ai_score += 1.5
        indicators.append(f"Multiple descriptive comments ({comment_count} found)")
    
    # Check for semantic HTML structure
    if '<header>' in code or '<section>' in code or '<article>' in code:
        ai_score += 0.5
        indicators.append("Semantic HTML5 elements")
    
    # Check for Bootstrap classes
    bootstrap_classes = ['container', 'row', 'col-', 'bg-', 'text-', 'mt-', 'mb-', 'p-']
    bootstrap_count = sum(1 for cls in bootstrap_classes if cls in code)
    if bootstrap_count >= 6:
        ai_score += 1
        indicators.append(f"Extensive Bootstrap utility classes ({bootstrap_count} types)")
    
    # Check for custom CSS
    if '<style>' in code and '@media' in code:
        ai_score += 1
        indicators.append("Custom CSS with media queries")
    
    # Check for consistent naming conventions
    if re.search(r'class="[a-z-]+"', code):
        ai_score += 0.5
        indicators.append("Consistent kebab-case naming")
    
    # Check for proper DOCTYPE and meta tags
    if '<!DOCTYPE html>' in code and 'viewport' in code:
        ai_score += 1
        indicators.append("Proper HTML5 structure with meta viewport")
    
    # Check for CDN links
    if 'cdn.jsdelivr.net' in code or 'cdnjs.cloudflare.com' in code:
        ai_score += 1
        indicators.append("CDN links for libraries")
    
    # Check for nested grid structures
    if code.count('<div class="row') >= 2:
        ai_score += 1
        indicators.append("Complex nested grid structure")
    
    # Check for accessibility considerations
    if 'lang="en"' in code and 'charset="UTF-8"' in code:
        ai_score += 0.5
        indicators.append("Accessibility and encoding attributes")
    
    return min(ai_score, 10), indicators

def analyze_code_structure(code):
    """Analyze the structure of the HTML code"""
    try:
        soup = BeautifulSoup(code, 'html.parser')
        results = {
            'has_doctype': code.strip().startswith('<!DOCTYPE html>'),
            'has_bootstrap_css': 'bootstrap' in code and '.css' in code,
            'has_bootstrap_js': 'bootstrap' in code and '.js' in code,
            'has_container': soup.find('div', class_=lambda x: x and 'container' in x) is not None,
            'row_count': len(soup.find_all('div', class_=lambda x: x and 'row' in x)),
            'has_custom_css': '<style>' in code,
            'has_media_query': '@media' in code,
            'col_elements': len(soup.find_all('div', class_=lambda x: x and 'col-' in x))
        }
        return results
    except:
        return None

# Streamlit UI
st.set_page_config(page_title="HTML Code Checker", page_icon="🔍", layout="wide")

st.title("🔍 HTML Code Checker")
st.markdown("Check if your HTML code matches the expected Bootstrap grid layout and analyze AI characteristics.")

# Create two columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Enter Your Code")
    user_code = st.text_area("Paste your HTML code here:", height=400, placeholder="Paste your HTML code...")

with col2:
    st.subheader("ℹ️ Information")
    st.info("This checker will:\n- Compare your code with the expected layout\n- Analyze structural elements\n- Rate AI-writing likelihood (0-10)")
    
    if st.button("🔍 Analyze Code", type="primary", use_container_width=True):
        if user_code.strip():
            st.session_state['analyze'] = True
        else:
            st.error("Please enter some code to analyze!")

# Analysis section
if 'analyze' in st.session_state and st.session_state['analyze'] and user_code.strip():
    st.divider()
    st.subheader("📊 Analysis Results")
    
    # Calculate similarity
    similarity = calculate_similarity(user_code, EXPECTED_HTML)
    
    # Structure analysis
    structure = analyze_code_structure(user_code)
    
    # AI indicators
    ai_score, ai_indicators = check_ai_indicators(user_code)
    
    # Display results in columns
    result_col1, result_col2, result_col3 = st.columns(3)
    
    with result_col1:
        st.metric("Code Similarity", f"{similarity * 100:.1f}%")
        if similarity >= 0.95:
            st.success("✅ Excellent match!")
        elif similarity >= 0.80:
            st.warning("⚠️ Good match with minor differences")
        else:
            st.error("❌ Significant differences detected")
    
    with result_col2:
        st.metric("AI Writing Score", f"{ai_score:.1f}/10")
        if ai_score >= 7:
            st.info("🤖 Highly likely AI-generated")
        elif ai_score >= 4:
            st.info("🤔 Possibly AI-assisted")
        else:
            st.info("👤 Likely human-written")
    
    with result_col3:
        if structure:
            structure_score = sum([
                structure['has_doctype'],
                structure['has_bootstrap_css'],
                structure['has_bootstrap_js'],
                structure['has_container'],
                structure['row_count'] >= 2,
                structure['has_custom_css'],
                structure['has_media_query'],
                structure['col_elements'] >= 6
            ])
            st.metric("Structure Score", f"{structure_score}/8")
    
    # Detailed analysis
    st.divider()
    
    detail_col1, detail_col2 = st.columns(2)
    
    with detail_col1:
        st.subheader("🏗️ Structure Analysis")
        if structure:
            st.write("**Elements Found:**")
            st.write(f"- DOCTYPE declaration: {'✅' if structure['has_doctype'] else '❌'}")
            st.write(f"- Bootstrap CSS: {'✅' if structure['has_bootstrap_css'] else '❌'}")
            st.write(f"- Bootstrap JS: {'✅' if structure['has_bootstrap_js'] else '❌'}")
            st.write(f"- Container div: {'✅' if structure['has_container'] else '❌'}")
            st.write(f"- Row elements: {structure['row_count']}")
            st.write(f"- Column elements: {structure['col_elements']}")
            st.write(f"- Custom CSS: {'✅' if structure['has_custom_css'] else '❌'}")
            st.write(f"- Media queries: {'✅' if structure['has_media_query'] else '❌'}")
        else:
            st.error("Could not parse HTML structure")
    
    with detail_col2:
        st.subheader("🤖 AI Indicators")
        if ai_indicators:
            st.write("**Detected Indicators:**")
            for indicator in ai_indicators:
                st.write(f"- {indicator}")
        else:
            st.write("No strong AI indicators detected")
    
    # Show differences if not exact match
    if similarity < 1.0:
        st.divider()
        st.subheader("📋 Code Comparison")
        with st.expander("View Expected Code"):
            st.code(EXPECTED_HTML, language='html')
        with st.expander("View Your Code"):
            st.code(user_code, language='html')

# Footer
st.divider()
st.caption("Made with Streamlit • HTML Code Checker v1.0")