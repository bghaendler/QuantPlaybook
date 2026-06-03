import katex from 'katex';

const latex = `d_1 = \\frac{\\ln(\\textcolor{#3b82f6}{100} / \\textcolor{#ec4899}{95}) + (\\textcolor{#10b981}{0.1} - \\textcolor{#06b6d4}{0.05} + \\textcolor{#8b5cf6}{0.2}^2/2)\\textcolor{#f59e0b}{0.62}}{\\textcolor{#8b5cf6}{0.2}\\sqrt{\\textcolor{#f59e0b}{0.62}}}`;

try {
  const html = katex.renderToString(latex);
  console.log("SUCCESS! Parsed string is long:", html.length);
} catch (e) {
  console.error("FAIL!", e);
}
