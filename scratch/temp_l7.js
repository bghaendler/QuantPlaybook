
    // Tab switching logic for CQF M3 L7
    window.switchM3L7Tab = function(tab) {
        const tabs = ['taxonomy', 'pde', 'reduction', 'discrete', 'guide', 'sandbox'];
        tabs.forEach(t => {
            const sec = document.getElementById('secM3L7' + t.charAt(0).toUpperCase() + t.slice(1));
            const btn = document.getElementById('tabM3L7' + t.charAt(0).toUpperCase() + t.slice(1));
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
            setTimeout(updateM3L7Simulation, 100);
        }
    };

    let m3l7ChartInstance = null;

    // Normal Cumulative Distribution Function
    function m3l7NormCdf(x) {
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

    // Box-Muller transform for normal distribution
    function m3l7RandomNormal() {
        let u = 0, v = 0;
        while(u === 0) u = Math.random(); 
        while(v === 0) v = Math.random();
        return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    }

    // Vanilla European Call Black-Scholes price
    function m3l7BsCall(S, E, T, r, vol) {
        if (T <= 0) return Math.max(S - E, 0);
        const d1 = (Math.log(S / E) + (r + 0.5 * vol * vol) * T) / (vol * Math.sqrt(T));
        const d2 = d1 - vol * Math.sqrt(T);
        return S * m3l7NormCdf(d1) - E * Math.exp(-r * T) * m3l7NormCdf(d2);
    }

    window.toggleM3L7Inputs = function() {
        const type = document.getElementById('selectM3L7Type').value;
        const panelB = document.getElementById('panelM3L7Barrier');
        const panelS = document.getElementById('panelM3L7Samples');

        if (type.startsWith('barrier')) {
            panelB.style.display = 'block';
            panelS.style.display = 'none';
        } else {
            panelB.style.display = 'none';
            panelS.style.display = 'block';
        }
        updateM3L7Simulation();
    };

    window.updateM3L7Simulation = function() {
        const S0 = parseFloat(document.getElementById('slideM3L7Stock').value);
        const E = parseFloat(document.getElementById('slideM3L7Strike').value);
        const vol = parseFloat(document.getElementById('slideM3L7Vol').value) / 100;
        const T = parseFloat(document.getElementById('slideM3L7Time').value);
        const type = document.getElementById('selectM3L7Type').value;
        const B = parseFloat(document.getElementById('slideM3L7Barrier').value);
        const N_samples = parseInt(document.getElementById('slideM3L7Samples').value);

        const r = 0.05; // Risk-free rate 5%

        // Update Labels
        document.getElementById('valM3L7Stock').innerText = S0.toFixed(0);
        document.getElementById('valM3L7Strike').innerText = E.toFixed(0);
        document.getElementById('valM3L7Vol').innerText = (vol * 100).toFixed(0) + "%";
        document.getElementById('valM3L7Time').innerText = T.toFixed(2) + (T === 1 ? " Year" : " Years");
        document.getElementById('valM3L7Barrier').innerText = B.toFixed(0);
        document.getElementById('valM3L7Samples').innerText = N_samples;

        // European Vanilla Price
        const vanillaPrice = m3l7BsCall(S0, E, T, r, vol);
        document.getElementById('outM3L7Vanilla').innerText = "$" + vanillaPrice.toFixed(2);

        // Simulation parameters
        const N_steps = 50;
        const dt = T / N_steps;
        const N_sim_paths = 500; // Background paths for statistics
        const N_plot_paths = 8;  // Foreground paths for display

        let paths = [];
        let timeSteps = [];
        for (let j = 0; j <= N_steps; j++) {
            timeSteps.push(j * dt);
        }

        let payoffSum = 0;
        let payoffSqSum = 0;

        for (let p = 0; p < N_sim_paths; p++) {
            let path = [S0];
            let S = S0;
            let sumS = S0;
            let hitBarrier = false;

            // Generate path steps
            for (let j = 1; j <= N_steps; j++) {
                const rand = m3l7RandomNormal();
                // Risk-neutral SDE
                S = S * Math.exp((r - 0.5 * vol * vol) * dt + vol * Math.sqrt(dt) * rand);
                path.push(S);
                sumS += S;

                // Check barrier hit
                if (type === 'barrier_uo' && S >= B) hitBarrier = true;
                if (type === 'barrier_ui' && S >= B) hitBarrier = true;
                if (type === 'barrier_do' && S <= B) hitBarrier = true;
                if (type === 'barrier_di' && S <= B) hitBarrier = true;
            }

            // Save the first N_plot_paths for drawing
            if (p < N_plot_paths) {
                paths.push({ path: path, hit: hitBarrier });
            }

            // Calculate payoffs
            let payoff = 0;
            if (type === 'asian_fixed') {
                // Fixed Strike Asian Call
                const avgS = sumS / (N_steps + 1);
                payoff = Math.max(avgS - E, 0);
            } else if (type === 'asian_float') {
                // Floating Strike Asian Call
                const avgS = sumS / (N_steps + 1);
                payoff = Math.max(S - avgS, 0);
            } else if (type === 'barrier_uo') {
                // Up-and-Out Call
                payoff = hitBarrier ? 0 : Math.max(S - E, 0);
            } else if (type === 'barrier_ui') {
                // Up-and-In Call
                payoff = hitBarrier ? Math.max(S - E, 0) : 0;
            } else if (type === 'barrier_do') {
                // Down-and-Out Call
                payoff = hitBarrier ? 0 : Math.max(S - E, 0);
            } else if (type === 'barrier_di') {
                // Down-and-In Call
                payoff = hitBarrier ? Math.max(S - E, 0) : 0;
            }

            payoffSum += payoff;
            payoffSqSum += payoff * payoff;
        }

        // Pricing values
        const price = Math.exp(-r * T) * (payoffSum / N_sim_paths);
        const variance = (payoffSqSum / N_sim_paths) - (payoffSum / N_sim_paths) * (payoffSum / N_sim_paths);
        const stdError = Math.exp(-r * T) * Math.sqrt(variance / N_sim_paths);

        document.getElementById('outM3L7Price').innerText = "$" + price.toFixed(2);
        document.getElementById('outM3L7Error').innerText = "$" + stdError.toFixed(3);

        // Summarize behavior inside card
        const elSummary = document.getElementById('m3l7OutcomeSummary');
        if (type.startsWith('asian')) {
            elSummary.innerHTML = `
                <strong>Behavior: Arithmetic Asian Call</strong><br>
                Estimated price: <strong>$${price.toFixed(2)}</strong> (Vanilla European Call: $${vanillaPrice.toFixed(2)}).<br>
                <span style="color:var(--accent); font-weight:700;">Taxonomy Insight:</span> The Asian option's payoff depends on the historical average asset price. Because the average of an asset is mathematically less volatile than the terminal asset price itself ($\sigma_{\\text{average}} < \\sigma_{\\text{underlying}}$), the option has a lower variance profile and is **always cheaper** than its equivalent European vanilla counterpart!
            `;
        } else {
            elSummary.innerHTML = `
                <strong>Behavior: Barrier Call</strong><br>
                Estimated price: <strong>$${price.toFixed(2)}</strong> (Vanilla European Call: $${vanillaPrice.toFixed(2)}).<br>
                <span style="color:#8b5cf6; font-weight:700;">Taxonomy Insight:</span> Barrier options represent weak path-dependency. For Out options (e.g. Up-and-Out), there is a significant risk of crossing the barrier and getting nullified, making them much **cheaper** than standard calls. For In options (e.g. Up-and-In), they only activate upon hitting the barrier, keeping their premium low.
            `;
        }

        renderM3L7Plot(timeSteps, paths, type, B);
    };

    function renderM3L7Plot(timeSteps, paths, type, barrierLevel) {
        const ctx = document.getElementById('m3l7ExoticChart');
        if (!ctx) return;

        const isDark = document.body.classList.contains('dark-theme');
        const gridColor = isDark ? 'rgba(255,255,255,0.07)' : 'rgba(0,0,0,0.05)';
        const tickColor = isDark ? '#94a3b8' : '#6b7280';
        
        let datasets = [];

        // Add Monte Carlo paths
        paths.forEach((pObj, idx) => {
            let borderColor = 'rgba(59, 130, 246, 0.45)'; // Default blue
            if (type.startsWith('barrier') && pObj.hit) {
                // If it crossed the barrier, mark it in red or faded purple
                borderColor = type.endsWith('o') ? 'rgba(239, 68, 68, 0.25)' : 'rgba(16, 185, 129, 0.5)';
            }
            datasets.push({
                label: 'Path ' + (idx + 1),
                data: pObj.path.map((y, i) => ({ x: timeSteps[i], y: y })),
                borderColor: borderColor,
                borderWidth: 1.5,
                showLine: true,
                pointRadius: 0,
                fill: false
            });
        });

        // Add Barrier Line if it is a barrier option
        if (type.startsWith('barrier')) {
            datasets.push({
                label: 'Barrier Level',
                data: timeSteps.map(t => ({ x: t, y: barrierLevel })),
                borderColor: '#ef4444',
                borderWidth: 2,
                borderDash: [5, 5],
                showLine: true,
                pointRadius: 0,
                fill: false
            });
        }

        if (m3l7ChartInstance) {
            m3l7ChartInstance.destroy();
        }

        m3l7ChartInstance = new Chart(ctx, {
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
                        title: { display: true, text: 'Time (Years)', font: { size: 9 }, color: tickColor },
                        ticks: { color: tickColor, font: { size: 8 } },
                        grid: { color: gridColor }
                    },
                    y: {
                        title: { display: true, text: 'Stock Price ($)', font: { size: 9 }, color: tickColor },
                        ticks: { color: tickColor, font: { size: 8 } },
                        grid: { color: gridColor }
                    }
                }
            }
        });
    }
