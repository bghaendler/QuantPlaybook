import os

OUT = "/Users/borjagarcia/Coursera/app/templates/sections"

# id, eyebrow title, page title, lede, [core topics], plain-english big picture, [plain english bullets (label, text)]
TOPICS = [
    ("cmm-advanced-calculus", "Advanced Calculus",
     "Advanced Calculus",
     "Multivariable differential and integral calculus &mdash; the engine room behind Greeks, gradients and the change-of-variables formulas that pricing relies on.",
     ["Limits, continuity and differentiability in $\\mathbb{R}^n$",
      "Partial derivatives, the gradient $\\nabla f$, Jacobians and Hessians",
      "Chain rule, implicit &amp; inverse function theorems",
      "Taylor's theorem in several variables; optimization with Lagrange multipliers",
      "Multiple integrals, change of variables and the Jacobian determinant"],
     "Advanced calculus generalizes the single-variable derivative and integral to functions of many variables &mdash; exactly what you need when a portfolio value depends on many risk factors at once.",
     [("Gradients &amp; Greeks", "First-order sensitivities (delta, rho, vega) are partial derivatives; the Hessian holds the second-order Greeks like gamma."),
      ("Taylor expansions", "P&amp;L attribution and risk approximations are just multivariable Taylor series truncated to a couple of terms.")]),

    ("cmm-linear-algebra", "Linear Algebra",
     "Linear Algebra",
     "Vectors, matrices and the spectral theory behind covariance, PCA, factor models and the numerical core of almost every quant library.",
     ["Vector spaces, bases, rank and linear independence",
      "Matrix algebra, determinants and inverses; solving $A\\mathbf{x}=\\mathbf{b}$",
      "Eigenvalues, eigenvectors and diagonalization",
      "Symmetric / positive-definite matrices and the spectral theorem",
      "Orthogonality, projections and the Gram&ndash;Schmidt process"],
     "Linear algebra is the language of data with many dimensions. Returns of many assets, yield-curve movements and correlation structures all live as vectors and matrices.",
     [("Covariance &amp; PCA", "A covariance matrix is symmetric positive semi-definite; its eigenvectors are the principal components driving the yield curve or equity returns."),
      ("Linear systems", "Calibration and least-squares fitting reduce to solving or inverting matrix equations &mdash; numerically and stably.")]),

    ("cmm-probability", "Probability",
     "Probability",
     "Sample spaces, random variables, distributions and limit theorems &mdash; the foundation under risk-neutral pricing, Monte Carlo and risk measurement.",
     ["Probability spaces, conditional probability and Bayes' theorem",
      "Random variables, expectation, variance and higher moments",
      "Key distributions: normal, lognormal, Poisson, exponential",
      "Joint distributions, covariance, correlation and copulas",
      "Law of Large Numbers &amp; the Central Limit Theorem"],
     "Probability quantifies uncertainty. Every price in a complete market is an expectation under a risk-neutral measure, and every risk number is a statement about a distribution's tail.",
     [("Expectations price options", "Risk-neutral valuation expresses an option price as a discounted expected payoff &mdash; an integral against a probability density."),
      ("CLT underpins Monte Carlo", "Simulation error shrinks like $1/\\sqrt{N}$ precisely because of the Central Limit Theorem.")]),

    ("cmm-numerical-analysis", "Numerical Analysis",
     "Numerical Analysis",
     "Turning equations into stable, accurate computations &mdash; root-finding, interpolation, quadrature and the finite-difference schemes that solve pricing PDEs.",
     ["Floating-point arithmetic, error propagation and conditioning",
      "Root-finding: bisection, Newton&ndash;Raphson, secant methods",
      "Interpolation &amp; curve fitting (splines, least squares)",
      "Numerical integration (quadrature) and differentiation",
      "Finite-difference schemes; stability, consistency and convergence"],
     "Numerical analysis is about getting trustworthy answers from a computer. The right method is fast and stable; the wrong one silently amplifies rounding error.",
     [("Implied vol solvers", "Backing out implied volatility is a root-finding problem solved with Newton or Brent's method."),
      ("Stability matters", "An explicit finite-difference pricer can blow up unless the time step respects a stability (CFL) condition.")]),

    ("cmm-vector-analysis", "Vector Analysis",
     "Vector Analysis",
     "Differential operators on fields &mdash; gradient, divergence and curl &mdash; together with the integral theorems that connect local rates of change to global flows.",
     ["Scalar &amp; vector fields; the operators $\\nabla,\\ \\nabla\\cdot,\\ \\nabla\\times$",
      "Line, surface and volume integrals",
      "Green's, Stokes' and the Divergence theorems",
      "Conservative fields, potentials and path independence",
      "Curvilinear coordinates (cylindrical, spherical)"],
     "Vector analysis describes quantities that have direction and how they flow, diffuse or circulate &mdash; the same diffusion operator that appears in the Black&ndash;Scholes PDE.",
     [("Diffusion &amp; the Laplacian", "The $\\nabla^2$ (Laplacian) term governs how option value or heat spreads out across space."),
      ("Conservation laws", "Divergence theorems turn a statement about flux through a boundary into a statement about sources inside.")]),

    ("cmm-pde", "Partial Differential Equations",
     "Partial Differential Equations",
     "Equations relating partial derivatives of a multivariable function &mdash; with the heat / diffusion equation as the direct ancestor of Black&ndash;Scholes.",
     ["Classification: elliptic, parabolic and hyperbolic PDEs",
      "The heat / diffusion equation and its fundamental solution",
      "Separation of variables and Fourier methods",
      "Method of characteristics for first-order PDEs",
      "The Black&ndash;Scholes PDE as a transformed heat equation"],
     "A PDE links how a quantity changes in time to how it changes in space. Option prices, interest-rate models and physical diffusion all obey parabolic PDEs of the same family.",
     [("Black&ndash;Scholes = heat equation", "A change of variables turns the Black&ndash;Scholes PDE into the classic heat equation, which has a known closed-form solution."),
      ("Boundary / final conditions", "The payoff at expiry is the 'final condition' that selects the unique solution from the PDE's whole family.")]),

    ("cmm-complex-variables", "Complex Variables",
     "Complex Variables",
     "Calculus of functions of a complex variable &mdash; analyticity, contour integration and residues, the machinery behind Fourier and characteristic-function option pricing.",
     ["Complex numbers, the Argand plane and Euler's formula",
      "Analytic (holomorphic) functions &amp; the Cauchy&ndash;Riemann equations",
      "Contour integration and Cauchy's integral theorem / formula",
      "Taylor and Laurent series; classifying singularities",
      "The residue theorem and evaluation of real integrals"],
     "Complex analysis gives astonishingly clean tools for integrals that look impossible on the real line &mdash; which is why Fourier-transform pricing leans on it so heavily.",
     [("Characteristic functions", "Carr&ndash;Madan and Heston pricing invert a characteristic function via a contour integral in the complex plane."),
      ("Residues do the work", "Closing a contour and summing residues evaluates the inversion integrals that produce option prices.")]),

    ("cmm-boundary-value-problems", "Boundary Value Problems",
     "Boundary Value Problems",
     "Differential equations with conditions imposed at the ends of a domain &mdash; eigenvalue problems, Sturm&ndash;Liouville theory and Green's functions.",
     ["Boundary vs. initial value problems; well-posedness",
      "Sturm&ndash;Liouville theory and orthogonal eigenfunctions",
      "Eigenvalue problems and Fourier-series solutions",
      "Green's functions and fundamental solutions",
      "Dirichlet, Neumann and Robin boundary conditions"],
     "Many pricing problems are not 'start here and march forward' but 'pin the value at the edges and fill in the middle' &mdash; that is a boundary value problem.",
     [("Barriers as boundaries", "A knock-out option imposes a value of zero on a barrier &mdash; a Dirichlet boundary condition on the pricing PDE."),
      ("Eigenfunction expansions", "Solutions are built as sums of orthogonal modes, the same idea as a Fourier series.")]),

    ("cmm-linear-systems", "Linear Systems",
     "Linear Systems",
     "Systems of linear differential equations and their qualitative behaviour &mdash; matrix exponentials, phase portraits and stability via eigenvalues.",
     ["Systems $\\dot{\\mathbf{x}} = A\\mathbf{x}$ and the matrix exponential $e^{At}$",
      "Eigenvalue / eigenvector solution structure",
      "Phase portraits: nodes, saddles, spirals and centres",
      "Stability classification from the spectrum of $A$",
      "Coupling to inhomogeneous forcing and resonance"],
     "When several quantities evolve together and influence each other, you get a coupled linear system. Its long-run behaviour is read directly off the eigenvalues of the coupling matrix.",
     [("Eigenvalues = fate", "Positive real parts mean blow-up, negative means decay, imaginary means oscillation &mdash; the whole stability story in one spectrum."),
      ("Mean reversion", "Multi-factor short-rate models are linear systems whose eigenvalues set the speed of mean reversion.")]),

    ("cmm-numbers-sets", "Numbers and Sets",
     "Numbers and Sets",
     "The logical bedrock of mathematics &mdash; sets, functions, proof techniques and the construction of the number systems everything else is built on.",
     ["Set operations, relations and equivalence classes",
      "Functions: injective, surjective, bijective; cardinality",
      "Logic, quantifiers and methods of proof (induction, contradiction)",
      "Construction of $\\mathbb{N},\\ \\mathbb{Z},\\ \\mathbb{Q},\\ \\mathbb{R},\\ \\mathbb{C}$",
      "Countability and the notion of infinity"],
     "Before you can do analysis you need to be precise about what numbers, sets and functions actually are, and how to prove a statement is true beyond doubt.",
     [("Rigour pays rent", "Knowing exactly when a function is invertible is what guarantees implied volatility is well-defined and unique."),
      ("Sets define domains", "A term sheet's '$[L,U)$ versus $[L,U]$' is a precise set statement with real legal consequences.")]),

    ("cmm-mathematical-analysis", "Mathematical Analysis",
     "Mathematical Analysis",
     "The rigorous theory of limits, continuity, convergence and integration &mdash; the proofs that make calculus, and therefore stochastic calculus, trustworthy.",
     ["Sequences, series and convergence tests",
      "$\\varepsilon$&ndash;$\\delta$ definitions of limits and continuity",
      "Uniform convergence and interchanging limits / integrals",
      "Differentiation and the Riemann &amp; Lebesgue integrals",
      "Metric spaces, completeness and the contraction mapping theorem"],
     "Analysis is the 'why it works' behind calculus. It tells you when you may swap a limit and an integral, or differentiate under an expectation &mdash; steps quant proofs take constantly.",
     [("Completeness of $\\mathbb{R}$", "The property that every Cauchy sequence converges is what licenses limits, derivatives and Brownian motion."),
      ("Fixed points", "The contraction mapping theorem guarantees iterative calibration schemes converge to a unique solution.")]),

    ("cmm-group-theory", "Group Theory",
     "Group Theory",
     "The abstract study of symmetry &mdash; groups, subgroups and homomorphisms &mdash; underlying conservation laws, transformations and modern cryptography.",
     ["Groups, subgroups, cosets and Lagrange's theorem",
      "Cyclic, symmetric and permutation groups",
      "Homomorphisms, isomorphisms and quotient groups",
      "Group actions and orbits",
      "Lie groups and continuous symmetries (a first look)"],
     "Group theory is the mathematics of symmetry: the operations you can perform on an object that leave its essential structure unchanged.",
     [("Symmetry &amp; invariants", "Continuous symmetries (Lie groups) generate the conserved quantities and invariant transformations used in PDE solution methods."),
      ("Foundations elsewhere", "The same algebraic structures underpin elliptic-curve cryptography securing modern financial infrastructure.")]),

    ("cmm-qualitative-ode", "Qualitative ODE Theory",
     "Qualitative Theory of Ordinary Differential Equations",
     "Understanding ODE solutions without solving them &mdash; existence, uniqueness, stability, fixed points and bifurcations.",
     ["Existence &amp; uniqueness (Picard&ndash;Lindel&ouml;f) theorems",
      "Equilibria, linearization and local stability",
      "Phase-plane analysis and nullclines",
      "Lyapunov functions and global stability",
      "Bifurcations and qualitative changes in dynamics"],
     "Often you cannot write a formula for the solution &mdash; but you can still say whether it settles down, blows up or oscillates. That is the qualitative theory.",
     [("Stability without formulas", "Linearizing around an equilibrium tells you if a perturbed system returns to rest or runs away."),
      ("Bifurcations = regime shifts", "A small parameter change can flip a model from stable to oscillatory &mdash; the mathematical face of a regime change.")]),

    ("cmm-stl", "STL",
     "Introduction to the Standard Template Library",
     "The C++ Standard Template Library &mdash; generic containers, iterators and algorithms that make production quant code fast, reusable and type-safe.",
     ["Containers: <code>vector</code>, <code>map</code>, <code>set</code>, <code>unordered_map</code>, <code>deque</code>",
      "Iterators and ranges as the glue between containers and algorithms",
      "Generic algorithms: <code>sort</code>, <code>accumulate</code>, <code>transform</code>, <code>find</code>",
      "Function objects, lambdas and predicates",
      "Templates, generic programming and complexity guarantees"],
     "The STL is a battle-tested toolbox of data structures and algorithms. Knowing it means you write less code, with fewer bugs, that runs at C++ speed &mdash; essential for pricing and risk engines.",
     [("Containers &amp; complexity", "Choosing <code>vector</code> vs. <code>map</code> vs. <code>unordered_map</code> is a complexity decision that can make a Monte Carlo engine fast or slow."),
      ("Algorithms over loops", "Expressing work as <code>std::transform</code> / <code>std::accumulate</code> is clearer, safer and easier to parallelize than hand-written loops.")]),

    ("cmm-perturbation-theory-2", "Perturbation Theory II",
     "Singular Perturbation Theory",
     "The sequel to regular perturbation theory &mdash; boundary layers, matched asymptotics, WKB and multiple-scales methods that fix where naive expansions break down.",
     ["Why regular perturbation fails: secular terms &amp; non-uniformity",
      "Boundary layers and inner / outer expansions",
      "Matched asymptotic expansions and the matching principle",
      "Method of multiple scales (two-timing)",
      "WKB approximation and applications to near-expiry option asymptotics"],
     "When the small parameter multiplies the highest derivative, or corrections grow without bound, regular perturbation theory falls apart. Singular methods rescue it by stitching together solutions on different scales.",
     [("Boundary layers", "Thin regions of rapid change &mdash; like an option's behaviour extremely close to expiry &mdash; need their own 'zoomed-in' inner solution."),
      ("Multiple scales", "Tracking a fast oscillation and a slow decay simultaneously removes the secular $t\\sin t$ blow-up seen in Perturbation Theory I.")]),
]

TEMPLATE = '''<div id="view-{id}" style="display: none; font-family: var(--font-family-sans);">
    <header style="margin-bottom: 2rem;">
        <p style="color: var(--accent); font-weight: 700; font-size: 0.8rem; text-transform: uppercase; margin: 0;">Mathematical Methods &bull; {eyebrow}</p>
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; border-bottom: none; padding-bottom: 0;">{title}</h1>
        <p style="color: #64748b; margin-top: 0.5rem;">{lede}</p>
    </header>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 2rem; align-items: stretch; margin-bottom: 2rem;">
        <!-- Left Side: Core Topics -->
        <div class="card" style="margin-bottom: 0; padding: 1.5rem;">
            <h3>Core Topics</h3>
            <ul style="line-height: 1.8;">
{topics}
            </ul>
        </div>
        <!-- Right Side: Plain English Notes -->
        <div class="card" style="margin-bottom: 0; background: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 8px; padding: 1.5rem;">
            <h3 style="margin-top: 0; color: #b45309; font-family: 'Inter', sans-serif; font-weight: 700;">Plain English Notes</h3>
            <p style="font-family: 'Inter', sans-serif; line-height: 1.6; color: #451a03; margin-bottom: 1rem;"><strong>The Big Picture:</strong> {bigpic}</p>
            <ul style="font-family: 'Inter', sans-serif; font-size: 0.95rem; line-height: 1.8; color: #451a03; padding-left: 1.2rem; margin: 0;">
{pebullets}
            </ul>
        </div>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent); background: var(--bg-subtle, #f8fafc);">
        <h3 style="margin-top:0;">Detailed Notes Coming Soon</h3>
        <p style="margin-bottom:0; color:#475569;">This module's full side-by-side derivations and worked examples are being prepared. The outline above maps the territory; lecture material will be added here as it is released.</p>
    </div>
</div>
'''

for (sid, eyebrow, title, lede, topics, bigpic, pebullets) in TOPICS:
    topics_html = "\n".join(
        '                <li>{}</li>'.format(t) for t in topics)
    pe_html = "\n".join(
        '                <li style="margin-bottom: 0.5rem;"><strong>{}:</strong> {}</li>'.format(label, text)
        for (label, text) in pebullets)
    out = TEMPLATE.format(id=sid, eyebrow=eyebrow, title=title, lede=lede,
                          topics=topics_html, bigpic=bigpic, pebullets=pe_html)
    path = os.path.join(OUT, "view-{}.html".format(sid))
    with open(path, "w") as f:
        f.write(out)
    print("wrote", path)
