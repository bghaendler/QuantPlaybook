
    // Tab switching logic for CQF M3 L6
    window.switchM3L6Tab = function(tab) {
        const tabs = ['types', 'vega', 'calibration', 'smiles', 'guide', 'sandbox'];
        tabs.forEach(t => {
            const sec = document.getElementById('secM3L6' + t.charAt(0).toUpperCase() + t.slice(1));
            const btn = document.getElementById('tabM3L6' + t.charAt(0).toUpperCase() + t.slice(1));
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
            setTimeout(updateM3L6Simulation, 100);
        }
    };

    let m3l6ArbChartInstance = null;

    // Normal Cumulative Distribution Function
    function m3l6NormCdf(x) {
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

    // Normal probability density function
    function m3l6NormPdf(x) {
        return (1 / Math.sqrt(2 * Math.PI)) * Math.exp(-0.5 * x * x);
    }

    // Box-Muller transform for normal distribution
    function m3l6RandomNormal() {
        let u = 0, v = 0;
        while(u === 0) u = Math.random(); 
        while(v === 0) v = Math.random();
        return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    }

    // Black-Scholes call option price
    function m3l6BsCall(S, E, T, r, vol) {
        if (T <= 1e-5) return Math.max(S - E, 0);
        const d1 = (Math.log(S / E) + (r + 0.5 * vol * vol) * T) / (vol * Math.sqrt(T));
        const d2 = d1 - vol * Math.sqrt(T);
        return S * m3l6NormCdf(d1) - E * Math.exp(-r * T) * m3l6NormCdf(d2);
    }

    // Black-Scholes call option delta
    function m3l6BsDelta(S, E, T, r, vol) {
        if (T <= 1e-5) return S > E ? 1 : 0;
        const d1 = (Math.log(S / E) + (r + 0.5 * vol * vol) * T) / (vol * Math.sqrt(T));
        return m3l6NormCdf(d1);
    }

    // Black-Scholes call option gamma
    function m3l6BsGamma(S, E, T, r, vol) {
        if (T <= 1e-5) return 0;
        const d1 = (Math.log(S / E) + (r + 0.5 * vol * vol) * T) / (vol * Math.sqrt(T));
        return m3l6NormPdf(d1) / (S * vol * Math.sqrt(T));
    }

    window.updateM3L6Simulation = function() {
        const S0 = parseFloat(document.getElementById('slideM3L6Stock').value);
        const E = parseFloat(document.getElementById('slideM3L6Strike').value);
        const volA = parseFloat(document.getElementById('slideM3L6VolA').value) / 100;
        const volI = parseFloat(document.getElementById('slideM3L6VolI').value) / 100;
        const mu = parseFloat(document.getElementById('slideM3L6Drift').value) / 100;
        const hedgeStrat = document.getElementById('selectM3L6Hedge').value;

        // Labels
        document.getElementById('valM3L6Stock').innerText = S0.toFixed(0);
        document.getElementById('valM3L6Strike').innerText = E.toFixed(0);
        document.getElementById('valM3L6VolA').innerText = (volA * 100).toFixed(0) + "%";
        document.getElementById('valM3L6VolI').innerText = (volI * 100).toFixed(0) + "%";
        document.getElementById('valM3L6Drift').innerText = (mu * 100).toFixed(1) + "%";

        const T = 0.5; // Expiry 6 months
        const r = 0.05; // Risk-free rate 5%
        const N_steps = 50;
        const dt = T / N_steps;
        const N_paths = 8;

        let pathsArb = [];
        let timeSteps = [];
        for (let j = 0; j <= N_steps; j++) {
            timeSteps.push(j * dt);
        }

        // Initialize BS option price profiles
        const Va_0 = m3l6BsCall(S0, E, T, r, volA);
        const Vi_0 = m3l6BsCall(S0, E, T, r, volI);
        const guaranteedProfitVal = Va_0 - Vi_0;

        for (let p = 0; p < N_paths; p++) {
            let S = S0;
            let portfolioArb = [];
            
            // Mark-to-market variables
            // Start long the option (bought at Vi_0) and short the Delta shares
            const delta_0 = hedgeStrat === 'actual' ? m3l6BsDelta(S0, E, T, r, volA) : m3l6BsDelta(S0, E, T, r, volI);
            let cash = -Vi_0 + delta_0 * S0;
            let currentDelta = delta_0;

            portfolioArb.push(0.0); // Profit starts at zero

            for (let j = 1; j <= N_steps; j++) {
                const t = j * dt;
                const t_remain = T - t;

                // Move stock using Forecast actual volatility (physical dynamics)
                const rand = m3l6RandomNormal();
                const dS = S * mu * dt + S * volA * Math.sqrt(dt) * rand;
                const prevS = S;
                S += dS;

                // Accumulate cash in bank with interest
                cash = cash * (1 + r * dt);

                // Option value changes under implied volatility
                const Vi_next = m3l6BsCall(S, E, t_remain, r, volI);

                // Calculate profit of the Delta Hedged Portfolio at this step
                // Portfolio value = Option price + Cash - delta * Stock
                const portVal = Vi_next + cash - currentDelta * S;
                portfolioArb.push(portVal);

                // Rehedge for the next step
                currentDelta = hedgeStrat === 'actual' ? m3l6BsDelta(S, E, t_remain, r, volA) : m3l6BsDelta(S, E, t_remain, r, volI);
                // Adjust cash balance for the rehedge shares adjustment
                const nextDelta = hedgeStrat === 'actual' ? m3l6BsDelta(S, E, t_remain, r, volA) : m3l6BsDelta(S, E, t_remain, r, volI);
                cash += (nextDelta - currentDelta) * S;
            }

            pathsArb.push(portfolioArb);
        }

        // Summary text explanation
        const elOutcome = document.getElementById('m3l6OutcomeSummary');
        if (hedgeStrat === 'actual') {
            elOutcome.innerHTML = `
                <strong>Strategy: Hedging with Actual Volatility ($\sigma_a$)</strong><br>
                Theoretical guaranteed profit: <strong>$${guaranteedProfitVal.toFixed(2)}</strong> (represented by $V(\\sigma_a) - V(\\sigma_i)$).<br>
                <span style="color:var(--accent); font-weight:700;">Wilmott Insight:</span> By hedging with the actual volatility, you are replicating a short position in a <em>correctly priced</em> option, perfectly canceling out the terminal payout. The paths are highly volatile during the lifetime of the option (exhibiting random mark-to-market fluctuations due to the $\mu - r$ drift terms), but converge to the exact same **deterministic final profit** at expiration!
            `;
        } else {
            elOutcome.innerHTML = `
                <strong>Strategy: Hedging with Implied Volatility ($\sigma_i$)</strong><br>
                Accumulated profit SDE: $d\Pi = \\frac{1}{2}(\\sigma_a^2 - \\sigma_i^2) S^2 \\Gamma^i dt$<br>
                <span style="color:#8b5cf6; font-weight:700;">Wilmott Insight:</span> By hedging with implied volatility, you balance the daily random fluctuations of option pricing with the stock. The portfolio's increment is **strictly positive at every step** (since $\\sigma_a > \\sigma_i$ and $\\Gamma \\ge 0$). However, the final profit is **highly path-dependent and uncertain** because option Gamma is non-constant and peaks severely near the strike!
            `;
        }

        renderM3L6ArbPlot(timeSteps, pathsArb, hedgeStrat, guaranteedProfitVal);
    };

    function renderM3L6ArbPlot(timeSteps, paths, strategy, targetProfit) {
        const ctx = document.getElementById('m3l6ArbChart');
        if (!ctx) return;

        const isDark = document.body.classList.contains('dark-theme');
        const gridColor = isDark ? 'rgba(255,255,255,0.07)' : 'rgba(0,0,0,0.05)';
        const tickColor = isDark ? '#94a3b8' : '#6b7280';
        
        let datasets = [];

        // Add Monte Carlo paths
        paths.forEach((path, idx) => {
            datasets.push({
                label: 'Path ' + (idx + 1),
                data: path.map((y, i) => ({ x: timeSteps[i], y: y })),
                borderColor: strategy === 'actual' ? 'rgba(59, 130, 246, 0.4)' : 'rgba(139, 92, 246, 0.4)',
                borderWidth: 1.5,
                showLine: true,
                pointRadius: 0,
                fill: false
            });
        });

        // Add reference lines for Actual strategy
        if (strategy === 'actual') {
            datasets.push({
                label: 'Guaranteed Profit Target',
                data: timeSteps.map(t => ({ x: t, y: targetProfit })),
                borderColor: '#ef4444',
                borderWidth: 2,
                borderDash: [6, 6],
                showLine: true,
                pointRadius: 0,
                fill: false
            });
        }

        if (m3l6ArbChartInstance) {
            m3l6ArbChartInstance.destroy();
        }

        m3l6ArbChartInstance = new Chart(ctx, {
            type: 'scatter',
            data: { datasets: datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        type: 'linear',
                        position: 'bottom',
                        title: { display: true, text: 'Time to Expiration (Years)', font: { size: 9 }, color: tickColor },
                        ticks: { color: tickColor, font: { size: 8 } },
                        grid: { color: gridColor }
                    },
                    y: {
                        title: { display: true, text: 'Mark-to-Market Profit ($)', font: { size: 9 }, color: tickColor },
                        ticks: { color: tickColor, font: { size: 8 } },
                        grid: { color: gridColor }
                    }
                }
            }
        });
    }
