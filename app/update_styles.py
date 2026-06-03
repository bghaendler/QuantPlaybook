import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new css styles
new_css = """        :root {
            --bg-color: #ffffff;
            --text-color: #37352f;
            --sidebar-bg: #f7f7f5;
            --sidebar-border: #edece9;
            --card-bg: #ffffff;
            --card-border: #e9e9e6;
            --accent: #2383e2;
            --primary-color: var(--accent);
            --accent-glow: rgba(35, 131, 226, 0.08);
            --secondary-accent: #4f46e5;
            --success: #0f766e;
            --warning: #b45309;
            --nav-hover: rgba(55, 53, 47, 0.04);
            --nav-active-bg: rgba(35, 131, 226, 0.06);
            --nav-active-text: #2383e2;
            --font-family-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            --font-family-serif: "Latin Modern Roman", "Georgia", serif;
            --card-shadow: 0 1px 3px rgba(15, 15, 15, 0.1), 0 1px 2px rgba(15, 15, 15, 0.06);
            --code-bg: #f2f1ee;
            --input-border: #cbd5e1;
            --input-bg: #ffffff;
            --metric-bg: #f8fafc;
            --loader-bg: rgba(255, 255, 255, 0.9);
        }

        body.dark-theme {
            --bg-color: #191919;
            --text-color: #e3e3e3;
            --sidebar-bg: #202020;
            --sidebar-border: #2c2c2c;
            --card-bg: #202020;
            --card-border: #2c2c2c;
            --accent: #2f81f7;
            --primary-color: var(--accent);
            --accent-glow: rgba(47, 129, 247, 0.15);
            --secondary-accent: #6366f1;
            --success: #14b8a6;
            --warning: #f59e0b;
            --nav-hover: rgba(255, 255, 255, 0.055);
            --nav-active-bg: rgba(47, 129, 247, 0.1);
            --nav-active-text: #2f81f7;
            --card-shadow: 0 1px 3px rgba(0, 0, 0, 0.5), 0 1px 2px rgba(0, 0, 0, 0.3);
            --code-bg: #2c2c2c;
            --input-border: #444c56;
            --input-bg: #252525;
            --metric-bg: #252525;
            --loader-bg: rgba(25, 25, 25, 0.9);
        }

        body {
            font-family: var(--font-family-serif);
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            height: 100vh;
            overflow: hidden;
            display: flex;
            transition: background 0.3s, color 0.3s;
        }

        /* Notion-Style Settings */
        .settings-container {
            position: absolute;
            top: 1.5rem;
            right: 2.5rem;
            z-index: 100;
        }

        .settings-trigger {
            background: transparent;
            border: none;
            color: #64748b;
            cursor: pointer;
            padding: 6px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background 0.2s, color 0.2s;
            outline: none;
        }

        .settings-trigger:hover {
            background: var(--nav-hover);
            color: var(--text-color);
        }

        .settings-trigger svg {
            width: 20px;
            height: 20px;
        }

        .settings-dropdown {
            position: absolute;
            top: calc(100% + 4px);
            right: 0;
            width: 240px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            box-shadow: var(--card-shadow);
            padding: 0.75rem;
            display: none;
            flex-direction: column;
            gap: 0.75rem;
            animation: fadeIn 0.15s cubic-bezier(0.16, 1, 0.3, 1);
            font-family: var(--font-family-sans);
            z-index: 101;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-4px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .settings-dropdown.show {
            display: flex;
        }

        .settings-dropdown-header {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8;
            font-weight: 600;
            margin-bottom: 0.25rem;
            padding-left: 0.25rem;
        }

        .settings-dropdown-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.25rem 0.25rem;
        }

        .settings-item-label {
            font-size: 0.85rem;
            color: var(--text-color);
            font-weight: 500;
        }

        /* Toggle Switch CSS */
        .toggle-switch {
            position: relative;
            display: inline-block;
            width: 36px;
            height: 20px;
        }

        .toggle-switch input {
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider-toggle {
            position: absolute;
            cursor: pointer;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: #cbd5e1;
            transition: .2s;
            border-radius: 20px;
        }

        .slider-toggle:before {
            position: absolute;
            content: "";
            height: 16px;
            width: 16px;
            left: 2px;
            bottom: 2px;
            background-color: white;
            transition: .2s;
            border-radius: 50%;
        }

        input:checked + .slider-toggle {
            background-color: var(--accent);
        }

        input:checked + .slider-toggle:before {
            transform: translateX(16px);
        }

        /* Segmented Control CSS */
        .segmented-control {
            display: flex;
            background: var(--nav-hover);
            border-radius: 6px;
            padding: 2px;
            border: 1px solid var(--card-border);
        }

        .segment-btn {
            background: transparent;
            border: none;
            font-size: 0.75rem;
            font-weight: 600;
            color: #64748b;
            padding: 3px 10px;
            border-radius: 4px;
            cursor: pointer;
            transition: background 0.15s, color 0.15s;
            outline: none;
        }

        .segment-btn.active {
            background: var(--card-bg);
            color: var(--text-color);
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }

        /* Text Size Scaling */
        body.small-text {
            font-size: 14px;
        }
        body.small-text .main-content {
            font-size: 0.92rem;
        }
        body.small-text h1 {
            font-size: 1.85rem;
        }
        body.small-text h2 {
            font-size: 1.25rem;
        }
        body.small-text .card p,
        body.small-text .quiz-interactive-card p,
        body.small-text .quiz-solution p {
            font-size: 0.95rem;
        }
        body.small-text .metric-value {
            font-size: 1.25rem;
        }

        /* Content Width Transition */
        .main-content-inner {
            max-width: 960px;
            width: 100%;
            margin: 0 auto;
            transition: max-width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        body.wide-text .main-content-inner {
            max-width: 96% !important;
        }

        /* Dark Mode Inline Style Mappings */
        body.dark-theme [style*="background: #ffffff"],
        body.dark-theme [style*="background: #fff"],
        body.dark-theme [style*="background:white"],
        body.dark-theme [style*="background: white"],
        body.dark-theme [style*="background:#ffffff"],
        body.dark-theme [style*="background:#fff"],
        body.dark-theme .quiz-interactive-card,
        body.dark-theme .card {
            background: var(--card-bg) !important;
            color: var(--text-color) !important;
            border-color: var(--card-border) !important;
        }

        body.dark-theme [style*="background: #f8fafc"],
        body.dark-theme [style*="background: #f9fafb"],
        body.dark-theme [style*="background:#f8fafc"],
        body.dark-theme [style*="background:#f9fafb"],
        body.dark-theme [style*="background-color: #f8fafc"],
        body.dark-theme [style*="background-color: #f9fafb"],
        body.dark-theme [style*="background: #eff6ff"],
        body.dark-theme [style*="background: #eff6ff !important"],
        body.dark-theme [style*="background:#eff6ff"] {
            background: var(--metric-bg) !important;
            color: var(--text-color) !important;
            border-color: var(--card-border) !important;
        }

        body.dark-theme [style*="background: #f0fdf4"],
        body.dark-theme [style*="background:#f0fdf4"] {
            background: #1b2e22 !important;
            color: #d1fae5 !important;
            border-left-color: #22c55e !important;
        }

        body.dark-theme [style*="background: #fffbeb"],
        body.dark-theme [style*="background:#fffbeb"] {
            background: #2e261f !important;
            color: #fef3c7 !important;
            border-left-color: #f59e0b !important;
        }

        body.dark-theme [style*="color: #1e293b"],
        body.dark-theme [style*="color: #334155"],
        body.dark-theme [style*="color: #475569"],
        body.dark-theme [style*="color: #0f172a"],
        body.dark-theme [style*="color:#1e293b"],
        body.dark-theme [style*="color:#334155"],
        body.dark-theme [style*="color:#475569"],
        body.dark-theme [style*="color:#0f172a"],
        body.dark-theme .quiz-interactive-card p,
        body.dark-theme .quiz-solution p {
            color: var(--text-color) !important;
        }

        body.dark-theme [style*="color: #64748b"],
        body.dark-theme [style*="color: #6b7280"],
        body.dark-theme [style*="color:#64748b"],
        body.dark-theme [style*="color:#6b7280"],
        body.dark-theme .quiz-interactive-card span[style*="color: #94a3b8"] {
            color: #94a3b8 !important;
        }

        body.dark-theme [style*="border: 1px solid #e2e8f0"],
        body.dark-theme [style*="border: 1px solid #cbd5e1"],
        body.dark-theme [style*="border:1px solid #e2e8f0"],
        body.dark-theme [style*="border:1px solid #cbd5e1"] {
            border-color: var(--card-border) !important;
        }

        body.dark-theme input[type="text"],
        body.dark-theme textarea,
        body.dark-theme select {
            background: var(--input-bg) !important;
            color: var(--text-color) !important;
            border-color: var(--input-border) !important;
        }

        body.dark-theme .quiz-solution div[style*="background: #ffffff"],
        body.dark-theme .quiz-solution div[style*="background:#ffffff"] {
            background: var(--card-bg) !important;
            border-color: var(--card-border) !important;
        }

        body.dark-theme details[style*="border: 1px solid #cbd5e1"],
        body.dark-theme details[style*="border: 1px solid #e2e8f0"] {
            border-color: var(--card-border) !important;
        }

        body.dark-theme details summary[style*="background: #f8fafc"] {
            background: var(--metric-bg) !important;
            color: var(--text-color) !important;
        }

        /* Quiz Styles */
        .quiz-card {
            border: 1px solid var(--card-border);
            border-radius: 8px;
            margin-bottom: 1rem;
            cursor: pointer;
            transition: all 0.2s ease;
            background: var(--card-bg);
        }

        .quiz-card:hover {
            border-color: var(--accent);
        }

        .quiz-question {
            font-size: 1.15rem;
            padding: 1.5rem;
            background: var(--metric-bg);
            border-radius: 8px;
            list-style-type: none;
            margin: 0;
            outline: none;
            line-height: 1.8;
            color: var(--text-color);
        }

        .quiz-question::-webkit-details-marker {
            display: none;
        }

        .quiz-solution {
            padding: 1.5rem 2rem;
            border-top: 1px solid var(--card-border);
            border-bottom-left-radius: 8px;
            border-bottom-right-radius: 8px;
            background: var(--card-bg);
        }

        .quiz-card[open] {
            box-shadow: var(--card-shadow);
        }

        .quiz-card[open] .quiz-question {
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
            background: var(--accent-glow);
            color: var(--accent);
        }

        .quiz-solution p {
            margin-top: 0;
            margin-bottom: 1.25rem;
            line-height: 1.8;
            font-size: 1.05rem;
        }

        .quiz-solution ul {
            margin-top: 0;
            padding-left: 2rem;
            margin-bottom: 1.5rem;
            line-height: 1.8;
            font-size: 1.05rem;
        }
        
        .quiz-solution ul li {
            margin-bottom: 0.75rem;
        }

        /* Collapsible Menu Styles */
        .sidebar details {
            margin-bottom: 0.25rem;
        }

        .sidebar summary {
            cursor: pointer;
            list-style: none;
            display: flex;
            align-items: center;
            position: relative;
            user-select: none;
            transition: color 0.2s;
            outline: none;
        }

        .sidebar summary::-webkit-details-marker {
            display: none;
        }

        .sidebar summary::before {
            content: '▶';
            font-size: 0.45rem;
            margin-right: 0.5rem;
            color: #94a3b8;
            transition: transform 0.2s ease-in-out;
            display: inline-block;
        }

        .sidebar details[open] > summary::before {
            transform: rotate(90deg);
        }
        
        .sidebar summary:hover {
            color: var(--accent) !important;
        }

        .sidebar .nav-group {
            padding-left: 0.5rem;
            border-left: 1px solid var(--sidebar-border);
            margin-left: 0.2rem;
            margin-top: 0.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        /* Sidebar Navigation */
        .sidebar {
            width: 320px;
            background: var(--sidebar-bg);
            border-right: 1px solid var(--sidebar-border);
            display: flex;
            flex-direction: column;
            overflow-y: auto;
            z-index: 10;
            padding: 2.5rem 1.5rem;
            transition: background 0.3s, border-color 0.3s;
        }

        .sidebar::-webkit-scrollbar {
            width: 6px;
        }

        .sidebar::-webkit-scrollbar-thumb {
            background: var(--sidebar-border);
            border-radius: 10px;
        }

        .course-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--text-color);
            margin: 0 0 0.25rem 0;
            font-family: var(--font-family-sans);
            letter-spacing: -0.01em;
        }

        .course-subtitle {
            font-size: 0.8rem;
            color: #94a3b8;
            margin-bottom: 2rem;
            font-weight: 500;
            font-family: var(--font-family-sans);
        }

        .nav-section-title {
            font-size: 0.72rem;
            text-transform: uppercase;
            color: #94a3b8;
            font-weight: 700;
            margin: 1.25rem 0 0.4rem 0;
            letter-spacing: 0.06em;
            font-family: var(--font-family-sans);
        }

        .nav-item {
            padding: 0.45rem 0.6rem;
            margin-bottom: 0.15rem;
            border-radius: 6px;
            color: var(--text-color);
            font-size: 0.88rem;
            cursor: pointer;
            transition: background 0.15s, color 0.15s;
            display: flex;
            align-items: center;
            text-decoration: none;
            font-family: var(--font-family-sans);
            font-weight: 500;
        }

        .nav-item:hover {
            background: var(--nav-hover);
            color: var(--text-color);
        }

        .sub-nav-item {
            padding: 0.45rem 0.6rem 0.45rem 1.5rem;
            margin-bottom: 0.15rem;
            border-radius: 6px;
            color: var(--text-color);
            font-size: 0.85rem;
            cursor: pointer;
            transition: background 0.15s, color 0.15s;
            display: flex;
            align-items: center;
            text-decoration: none;
            font-family: var(--font-family-sans);
            position: relative;
        }

        .sub-nav-item:hover {
            background: var(--nav-hover);
            color: var(--text-color);
        }

        .sub-nav-item.active {
            background: var(--nav-active-bg);
            color: var(--nav-active-text);
            font-weight: 600;
        }

        .nav-item.active {
            background: var(--nav-active-bg);
            color: var(--nav-active-text);
            font-weight: 600;
        }

        .badge {
            font-size: 0.65rem;
            font-weight: 800;
            padding: 2px 6px;
            border-radius: 12px;
            text-transform: uppercase;
        }

        .badge-done {
            background: rgba(16, 185, 129, 0.2);
            color: #34d399;
        }

        .badge-pending {
            background: rgba(245, 158, 11, 0.2);
            color: #fbbf24;
        }

        .badge-video {
            background: rgba(255, 255, 255, 0.1);
            color: #94a3b8;
        }

        /* Main Content */
        .main-content {
            flex: 1;
            overflow-y: auto;
            position: relative;
            padding: 3.5rem 4rem;
            scroll-behavior: smooth;
            background: var(--bg-color);
            color: var(--text-color);
            transition: background 0.3s, color 0.3s;
        }

        header {
            margin-bottom: 2rem;
        }

        h1 {
            font-size: 2.2rem;
            font-weight: 800;
            margin: 0 0 0.5rem 0;
            color: var(--text-color);
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 1rem;
        }

        h2 {
            font-size: 1.4rem;
            font-weight: 600;
            color: var(--text-color);
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }

        .container {
            max-width: 100%;
            display: grid;
            grid-template-columns: 1fr;
            gap: 2rem;
            margin-bottom: 4rem;
        }

        @media (min-width: 1200px) {
            .container {
                grid-template-columns: 1fr 1fr;
            }
        }

        .card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 2rem;
            box-shadow: var(--card-shadow);
            margin-bottom: 2rem;
            transition: background 0.3s, border-color 0.3s;
        }

        .card p {
            line-height: 1.8;
            margin-bottom: 1.25rem;
        }

        .metric {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            margin-bottom: 1rem;
            background: var(--metric-bg);
            border-radius: 6px;
            border-left: 4px solid var(--accent);
            font-family: var(--font-family-sans);
            transition: background 0.3s;
        }

        .metric.secondary {
            border-left-color: var(--secondary-accent);
        }

        .metric-label {
            font-weight: 600;
            color: var(--text-color);
            opacity: 0.85;
        }

        .metric-value {
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--text-color);
        }

        .chart-container {
            position: relative;
            height: 300px;
            width: 100%;
            margin-top: 1.5rem;
        }

        /* Loader */
        #loader {
            position: fixed;
            top: 50%;
            left: 60%;
            transform: translate(-50%, -50%);
            display: flex;
            flex-direction: column;
            align-items: center;
            color: var(--accent);
            z-index: 100;
            background: var(--loader-bg);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: var(--card-shadow);
        }

        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid var(--accent-glow);
            border-top-color: var(--accent);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 1rem;
        }

        @keyframes spin {
            100% {
                transform: rotate(360deg);
            }
        }

        #dashboard {
            display: none;
        }

        .view-placeholder {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 60vh;
            text-align: center;
            color: #64748b;
        }

        .view-placeholder svg {
            width: 64px;
            height: 64px;
            margin-bottom: 1rem;
            opacity: 0.5;
        }

        /* SVG icons spacing */
        .sidebar-icon {
            width: 14px;
            height: 14px;
            margin-right: 8px;
            flex-shrink: 0;
            color: #94a3b8;
            transition: color 0.2s;
        }

        .nav-item.active .sidebar-icon,
        .sub-nav-item.active .sidebar-icon {
            color: var(--accent) !important;
        }

        .sidebar summary:hover .sidebar-icon {
            color: var(--accent) !important;
        }

        .coursera-section {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
            margin-bottom: 0.8rem;
            border-bottom: 1px solid var(--sidebar-border);
            padding-bottom: 0.8rem;
        }
        .coursera-section:last-child {
            border-bottom: none;
            padding-bottom: 0;
            margin-bottom: 0;
        }
        .coursera-section-header {
            font-size: 0.8rem;
            font-weight: 700;
            color: #475569;
            margin-bottom: 0.5rem;
            padding-left: 0.25rem;
            font-family: var(--font-family-sans);
            text-transform: none;
        }
        .coursera-nav-item {
            display: flex;
            align-items: flex-start;
            padding: 0.6rem 0.5rem;
            text-decoration: none;
            color: inherit;
            border-radius: 6px;
            transition: all 0.2s ease;
            cursor: pointer;
            margin-bottom: 0.15rem;
            font-family: var(--font-family-sans);
        }
        .coursera-nav-item:hover {
            background-color: var(--nav-hover);
        }
        .coursera-nav-item.active {
            background-color: var(--nav-active-bg) !important;
            color: var(--nav-active-text) !important;
        }
        .coursera-icon {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 0.6rem;
            margin-top: 0.1rem;
            flex-shrink: 0;
        }
        .icon-checked {
            background-color: #15803d;
            position: relative;
        }
        .icon-checked::after {
            content: '';
            position: absolute;
            left: 6px;
            top: 3px;
            width: 4px;
            height: 8px;
            border: solid white;
            border-width: 0 2px 2px 0;
            transform: rotate(45deg);
        }
        .icon-pending {
            background-color: var(--input-bg);
            border: 2px solid var(--sidebar-border);
        }
        .coursera-info {
            display: flex;
            flex-direction: column;
            gap: 1px;
        }
        .coursera-title {
            font-size: 0.85rem;
            font-weight: 500;
            color: var(--text-color);
            line-height: 1.25;
            transition: color 0.2s;
        }
        .coursera-meta {
            font-size: 0.75rem;
            color: #64748b;
            font-weight: 400;
            transition: color 0.2s;
        }
        .coursera-nav-item.active .coursera-title {
            color: var(--nav-active-text) !important;
            font-weight: 600;
        }
        .coursera-nav-item.active .coursera-meta {
            color: var(--accent) !important;
        }"""

# Replace the text inside <style>...</style> using regex
pattern = r"(<style>).*?(</style>)"
updated_content, count = re.subn(pattern, r"\1\n" + new_css + r"\n\2", content, flags=re.DOTALL)

if count > 0:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print(f"CSS updated successfully in index.html! Made {count} replacements.")
else:
    print("Could not find style tags in index.html using regex!")
