
    // Tab switching logic for CQF M3 L5
    window.switchM3L5Tab = function(tab) {
        const tabs = ['implicit', 'crankNic', 'algebra', 'advanced', 'guide', 'sandbox'];
        tabs.forEach(t => {
            const sec = document.getElementById('secM3L5' + t.charAt(0).toUpperCase() + t.slice(1));
            const btn = document.getElementById('tabM3L5' + t.charAt(0).toUpperCase() + t.slice(1));
            if (sec) {
                sec.style.display = (t === tab ? 'block' : 'none');
                if (t === tab && !sec.dataset.typeset) {
                    if (typeof window.safeTypeset === 'function') {
                        window.safeTypeset([sec]);
                        sec.dataset.typeset = 'true';
                    }
                }
            }
            if (btn) {
                if (t === tab) {
                    btn.style.color = 'var(--accent)';
                    btn.style.borderBottom = '2px solid var(--accent)';
                    btn.style.fontWeight = '700';
                } else {
                    btn.style.color = '#6b7280';
                    btn.style.borderBottom = '2px solid transparent';
                    btn.style.fontWeight = '600';
                }
            }
        });

        if (tab === 'sandbox') {
            setTimeout(updateM3L5Sandbox, 100);
        }
    };

    let m3l5GridChartInstance = null;

    // Normal Cumulative Distribution Function
    function m3l5NormCdf(x) {
        const b1 =  0.319381530;
        const b2 = -0.356563782;
        const b3 =  1.781477937;
        const b4 = -1.821255978;
        const b5 =  1.330274429;
        const p  =  0.2316419;
        const c  =  0.39894228;

        if (x >= 0.0) {
            let k = 1.0 / (1.0 + p * x);
            return 1.0 - c * Math.exp(-x * x / 2.0) * k * (k * (k * (k * (k * b5 + b4) + b3) + b2) + b1);
        } else {
            let k = 1.0 / (1.0 - p * x);
            return c * Math.exp(-x * x / 2.0) * k * (k * (k * (k * (k * b5 + b4) + b3) + b2) + b1);
        }
    }

    // Thomas Tridiagonal Solver LU algorithm in JS
    // Solves system M * v = q, where M coefficients are: sub-diag 'a', diag 'b', super-diag 'c'
    function solveTridiagonalThomas(a, b, c, q, I) {
        let d = Array(I).fill(0);
        let l = Array(I).fill(0);
        let u = Array(I).fill(0);
        
        // Forward Sweep to decompose bidiagonal coefficients
        d[1] = b[1];
        for (let i = 2; i < I; i++) {
            l[i] = a[i] / d[i-1];
            u[i-1] = c[i-1];
            d[i] = b[i] - l[i] * u[i-1];
        }

        // Forward Substitution LW = Q
        let w = Array(I).fill(0);
        w[1] = q[1];
        for (let i = 2; i < I; i++) {
            w[i] = q[i] - l[i] * w[i-1];
        }

        // Backward Substitution UV = W
        let v = Array(I).fill(0);
        v[I-1] = w[I-1] / d[I-1];
        for (let i = I - 2; i >= 1; i--) {
            v[i] = (w[i] - u[i] * v[i+1]) / d[i];
        }

        return v;
    }

    window.updateM3L5Sandbox = function() {
        const S0 = parseFloat(document.getElementById('slideM3L5Stock').value);
        const E = parseFloat(document.getElementById('slideM3L5Strike').value);
        const vol = parseFloat(document.getElementById('slideM3L5Vol').value) / 100;
        const T = parseFloat(document.getElementById('slideM3L5Time').value);
        const r = parseFloat(document.getElementById('slideM3L5Rate').value) / 100;
        const N = parseInt(document.getElementById('slideM3L5Nodes').value);

        // Labels
        document.getElementById('valM3L5Stock').innerText = S0.toFixed(0);
        document.getElementById('valM3L5Strike').innerText = E.toFixed(0);
        document.getElementById('valM3L5Vol').innerText = (vol * 100).toFixed(0) + "%";
        document.getElementById('valM3L5Time').innerText = T.toFixed(2) + (T === 1 ? " Year" : " Years");
        document.getElementById('valM3L5Rate').innerText = (r * 100).toFixed(1) + "%";
        document.getElementById('valM3L5Nodes').innerText = N;

        // BS Analytical
        const d1 = (Math.log(S0 / E) + (r + 0.5 * vol * vol) * T) / (vol * Math.sqrt(T));
        const d2 = d1 - vol * Math.sqrt(T);
        const bsPrice = S0 * m3l5NormCdf(d1) - E * Math.exp(-r * T) * m3l5NormCdf(d2);
        document.getElementById('outM3L5BsPrice').innerText = "$" + bsPrice.toFixed(2);

        // Grid specifications
        const S_max = 200;
        const dS = S_max / N;

        // Dynamic M_steps to guarantee explicit stability limit
        const stableDt = 0.9 / (vol * vol * N * N);
        let M_steps = Math.ceil(T / stableDt);
        if (M_steps < 40) M_steps = 40; // minimum steps
        const dt = T / M_steps;

        // --- 1. Explicit Solver ---
        let expGrid = [];
        for (let i = 0; i <= N; i++) expGrid[i] = Math.max(i * dS - E, 0); // terminals
        for (let k = 1; k <= M_steps; k++) {
            let nextGrid = [];
            nextGrid[0] = (1 - r * dt) * expGrid[0];
            for (let i = 1; i < N; i++) {
                const alpha = 0.5 * (vol * vol * i * i - i * r) * dt;
                const beta = 1 - (vol * vol * i * i + r) * dt;
                const gamma = 0.5 * (vol * vol * i * i + i * r) * dt;
                nextGrid[i] = alpha * expGrid[i-1] + beta * expGrid[i] + gamma * expGrid[i+1];
            }
            nextGrid[N] = 2 * nextGrid[N-1] - nextGrid[N-2];
            expGrid = nextGrid;
        }

        // --- 2. Fully Implicit Solver ---
        let impGrid = [];
        for (let i = 0; i <= N; i++) impGrid[i] = Math.max(i * dS - E, 0); // terminals
        for (let k = 1; k <= M_steps; k++) {
            // Setup Tridiagonal vectors
            let a = Array(N + 1).fill(0);
            let b = Array(N + 1).fill(0);
            let c = Array(N + 1).fill(0);
            let q = Array(N + 1).fill(0);

            for (let i = 1; i < N; i++) {
                a[i] = -0.5 * (vol * vol * i * i - i * r) * dt;
                b[i] = 1 + (vol * vol * i * i + r) * dt;
                c[i] = -0.5 * (vol * vol * i * i + i * r) * dt;
                q[i] = impGrid[i];
            }

            // Boundary condition injection
            impGrid[0] = impGrid[0] / (1 + r * dt);
            q[1] -= a[1] * impGrid[0];

            // vanishing gamma boundary condition S_max
            // V[N] = 2*V[N-1] - V[N-2]. Substitute this inside row N-1 equation:
            // a*V[N-2] + b*V[N-1] + c*(2*V[N-1] - V[N-2]) = q
            // (a - c)*V[N-2] + (b + 2c)*V[N-1] = q
            a[N-1] -= c[N-1];
            b[N-1] += 2 * c[N-1];

            // Solve using Thomas Algorithm
            const solvedV = solveTridiagonalThomas(a, b, c, q, N);
            
            // Populate grid
            for (let i = 1; i < N; i++) {
                impGrid[i] = solvedV[i];
            }
            impGrid[N] = 2 * impGrid[N-1] - impGrid[N-2];
        }

        // --- 3. Crank-Nicolson Solver ---
        let cnGrid = [];
        for (let i = 0; i <= N; i++) cnGrid[i] = Math.max(i * dS - E, 0); // terminals
        for (let k = 1; k <= M_steps; k++) {
            let a = Array(N + 1).fill(0);
            let b = Array(N + 1).fill(0);
            let c = Array(N + 1).fill(0);
            let q = Array(N + 1).fill(0);

            for (let i = 1; i < N; i++) {
                // Left Hand Side (Implicit matrix coefficients)
                a[i] = -0.25 * (vol * vol * i * i - i * r) * dt;
                b[i] = 1 + 0.5 * (vol * vol * i * i + r) * dt;
                c[i] = -0.25 * (vol * vol * i * i + i * r) * dt;

                // Right Hand Side (Explicit matrix coefficients times current grid)
                const alpha_ex = 0.25 * (vol * vol * i * i - i * r) * dt;
                const beta_ex = 1 - 0.5 * (vol * vol * i * i + r) * dt;
                const gamma_ex = 0.25 * (vol * vol * i * i + i * r) * dt;

                q[i] = alpha_ex * cnGrid[i-1] + beta_ex * cnGrid[i] + gamma_ex * cnGrid[i+1];
            }

            // Boundary conditions
            const cnGrid_0_next = cnGrid[0] * (1 - 0.5 * r * dt) / (1 + 0.5 * r * dt);
            q[1] -= a[1] * cnGrid_0_next;

            // vanishing gamma boundary
            a[N-1] -= c[N-1];
            b[N-1] += 2 * c[N-1];

            // Solve Crank-Nicolson Tridiagonal
            const solvedV = solveTridiagonalThomas(a, b, c, q, N);

            cnGrid[0] = cnGrid_0_next;
            for (let i = 1; i < N; i++) {
                cnGrid[i] = solvedV[i];
            }
            cnGrid[N] = 2 * cnGrid[N-1] - cnGrid[N-2];
        }

        // Interpolate Spot Prices
        const S0_idx = S0 / dS;
        const low = Math.floor(S0_idx);
        const high = Math.ceil(S0_idx);
        const lerp = (lowPrice, highPrice) => lowPrice + (S0_idx - low) * (highPrice - lowPrice);

        document.getElementById('outM3L5Explicit').innerText = "$" + lerp(expGrid[low], expGrid[high]).toFixed(2);
        document.getElementById('outM3L5Implicit').innerText = "$" + lerp(impGrid[low], impGrid[high]).toFixed(2);
        document.getElementById('outM3L5CrankNic').innerText = "$" + lerp(cnGrid[low], cnGrid[high]).toFixed(2);

        // Generate Plot points to display asset profile
        let spots = [];
        let expData = [];
        let impData = [];
        let cnData = [];
        
        for (let i = 0; i <= N; i++) {
            spots.push(i * dS);
            expData.push(expGrid[i]);
            impData.push(impGrid[i]);
            cnData.push(cnGrid[i]);
        }

        renderM3L5GridPlot(spots, expData, impData, cnData);
    };

    function renderM3L5GridPlot(spots, explicitData, implicitData, cnData) {
        const ctx = document.getElementById('m3l5GridChart');
        if (!ctx) return;

        const spotLabels = spots.map(s => s.toFixed(0));

        const datasets = [
            {
                label: 'Explicit FDM',
                data: explicitData,
                borderColor: 'var(--text-color)',
                borderWidth: 1.5,
                fill: false,
                pointRadius: 0
            },
            {
                label: 'Fully Implicit FDM',
                data: implicitData,
                borderColor: 'var(--accent)',
                borderWidth: 2,
                fill: false,
                pointRadius: 0
            },
            {
                label: 'Crank-Nicolson FDM',
                data: cnData,
                borderColor: '#8b5cf6',
                borderWidth: 2,
                fill: false,
                pointRadius: 0
            }
        ];

        if (m3l5GridChartInstance) {
            m3l5GridChartInstance.data.labels = spotLabels;
            m3l5GridChartInstance.data.datasets = datasets;
            m3l5GridChartInstance.update();
            return;
        }

        m3l5GridChartInstance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: spotLabels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: true, position: 'bottom', labels: { boxWidth: 10, font: { size: 8 } } }
                },
                scales: {
                    x: {
                        title: { display: true, text: 'Stock Price ($)', font: { size: 9 } },
                        ticks: { font: { size: 8 } }
                    },
                    y: {
                        title: { display: true, text: 'Option Value ($)', font: { size: 9 } },
                        ticks: { font: { size: 8 } }
                    }
                }
            }
        });
    }
