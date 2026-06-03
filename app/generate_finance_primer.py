import os

output_dir = "/Users/borjagarcia/Coursera/app/templates/sections"
os.makedirs(output_dir, exist_ok=True)

# Helper function to generate common head structure
def make_header(title, badge1="Finance Primer", badge2="Financial Markets"):
    return f"""<div id="view-cqf-fp-{title.lower().replace(' ', '-').replace('&', 'and').replace(',', '').replace('(', '').replace(')', '')}" style="display: none; font-family: var(--font-family-sans);">
    <header style="margin-bottom: 2rem;">
        <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
            <span class="badge" style="background: rgba(79, 70, 229, 0.1); color: #4f46e5; font-weight: 700; font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 20px; border: 1px solid #4f46e5;">{badge1}</span>
            <span class="badge" style="background: rgba(14, 165, 233, 0.1); color: #0ea5e9; font-weight: 700; font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 20px; border: 1px solid #0ea5e9;">{badge2}</span>
        </div>
        <h1 style="margin: 0; font-size: 2rem; font-weight: 800; border-bottom: none; padding-bottom: 0;">{title}</h1>
    </header>"""

# Define templates
pages = {}

# 1. Commodities Intro
pages["view-cqf-fp-commodities.html"] = make_header("Introduction to Commodities", badge2="Commodities") + """
    <div class="card">
        <h3>1.1 Understanding Commodity Markets</h3>
        <p>Investors allocate capital not just in financial instruments but also in physical commodity markets. Unlike standard equities, commodities involve producers, processors, consumers, and physical supply chains as raw materials change form.</p>
        
        <h4>Key Theoretical Terminology:</h4>
        <ul>
            <li><strong>Contango:</strong> A market condition where the futures price of a commodity is higher than the spot price. This usually occurs due to storage costs, insurance, and carry fees.</li>
            <li><strong>Backwardation:</strong> A condition where the futures price is lower than the spot price. This often signals near-term supply shortages or a high <em>convenience yield</em>.</li>
        </ul>
        
        <p>$$ F(t, T) = S(t) e^{(r + w - c)(T - t)} $$</p>
        <p>Where $r$ is the risk-free rate, $w$ is storage costs, and $c$ is the convenience yield.</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Backwardation &amp; Contango Sandbox</h3>
        <p>Adjust the storage costs and convenience yield to observe how the term structure curve shifts between Contango and Backwardation.</p>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Storage Costs ($w$):</label>
                <input id="commStorage" type="range" min="0" max="0.1" step="0.01" value="0.03" oninput="calcCommCurve()" style="width: 100%;">
                <span id="commStorageVal" style="font-size: 0.85rem; font-weight: 700; color: var(--accent);">3%</span>
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Convenience Yield ($c$):</label>
                <input id="commConv" type="range" min="0" max="0.15" step="0.01" value="0.01" oninput="calcCommCurve()" style="width: 100%;">
                <span id="commConvVal" style="font-size: 0.85rem; font-weight: 700; color: var(--accent);">1%</span>
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border);">
            <h4 style="margin-top: 0; color: var(--accent);">Term Structure Forecast (Spot = $100):</h4>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                <thead>
                    <tr style="border-bottom: 1px solid var(--card-border); text-align: left;">
                        <th style="padding: 0.5rem;">Maturity</th>
                        <th style="padding: 0.5rem;">Futures Price</th>
                        <th style="padding: 0.5rem;">Market State</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 0.5rem;">Spot</td>
                        <td style="padding: 0.5rem;">$100.00</td>
                        <td style="padding: 0.5rem;">-</td>
                    </tr>
                    <tr>
                        <td style="padding: 0.5rem;">3 Months</td>
                        <td id="commF3" style="padding: 0.5rem; font-weight: 700;">$100.50</td>
                        <td id="commState3" style="padding: 0.5rem;">Contango</td>
                    </tr>
                    <tr>
                        <td style="padding: 0.5rem;">1 Year</td>
                        <td id="commF12" style="padding: 0.5rem; font-weight: 700;">$102.02</td>
                        <td id="commState12" style="padding: 0.5rem;">Contango</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<script>
function calcCommCurve() {
    const s = 100;
    const r = 0.02;
    const w = parseFloat(document.getElementById('commStorage').value);
    const c = parseFloat(document.getElementById('commConv').value);
    
    document.getElementById('commStorageVal').innerText = (w * 100).toFixed(0) + '%';
    document.getElementById('commConvVal').innerText = (c * 100).toFixed(0) + '%';
    
    const rate = r + w - c;
    const f3 = s * Math.exp(rate * 0.25);
    const f12 = s * Math.exp(rate * 1.0);
    
    document.getElementById('commF3').innerText = '$' + f3.toFixed(2);
    document.getElementById('commF12').innerText = '$' + f12.toFixed(2);
    
    const state = rate >= 0 ? '<span style="color:#10b981;font-weight:700;">Contango</span>' : '<span style="color:#ef4444;font-weight:700;">Backwardation</span>';
    document.getElementById('commState3').innerHTML = state;
    document.getElementById('commState12').innerHTML = state;
}
setTimeout(calcCommCurve, 500);
</script>
"""

# 2. Futures and Forwards Applications
pages["view-cqf-fp-deriv-futures-apps.html"] = make_header("Futures & Forwards Applications", badge2="Derivatives") + """
    <div class="card">
        <h3>2.1 Hedging vs. Speculation</h3>
        <p>Derivatives such as futures and forwards serve two core economic functions:</p>
        <ul>
            <li><strong>Hedging:</strong> Reducing pricing uncertainty by locking in trade rates. A wheat farmer hedges against falling crop prices, while a processor locks in purchases.</li>
            <li><strong>Speculation:</strong> Expressing direction views on the asset without physical delivery to profit from favorable movements.</li>
        </ul>
        <p>Payout of a Long Futures position: $$ \Pi_{\text{long}} = S_T - F_0 $$</p>
        <p>Payout of a Short Futures position: $$ \Pi_{\text{short}} = F_0 - S_T $$</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Hedging vs. Speculation Simulator</h3>
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Locked-in Futures Price ($F_0$):</label>
                <input id="futAppF0" type="number" value="50" style="padding: 0.4rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcFutApp()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Settlement Spot Price ($S_T$):</label>
                <input id="futAppST" type="range" min="30" max="70" value="55" style="width: 100%;" oninput="calcFutApp()">
                <span id="futAppSTVal" style="font-size: 0.85rem; font-weight: 700; color: var(--accent);">$55</span>
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1rem; border-radius: 8px; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="border-right: 1px solid var(--card-border); padding-right: 1rem;">
                <h4 style="color: #4f46e5; margin-top: 0;">Long Speculator Payout</h4>
                <div id="futLongPayout" style="font-size: 1.5rem; font-weight: 800; color: #10b981;">+$5.00</div>
            </div>
            <div style="padding-left: 1rem;">
                <h4 style="color: #ef4444; margin-top: 0;">Short Hedger (Farmer) Payout</h4>
                <div id="futShortPayout" style="font-size: 1.5rem; font-weight: 800; color: #ef4444;">-$5.00</div>
            </div>
        </div>
    </div>
</div>

<script>
function calcFutApp() {
    const f0 = parseFloat(document.getElementById('futAppF0').value) || 0;
    const st = parseFloat(document.getElementById('futAppST').value);
    document.getElementById('futAppSTVal').innerText = '$' + st;
    
    const longP = st - f0;
    const shortP = f0 - st;
    
    document.getElementById('futLongPayout').innerText = (longP >= 0 ? '+' : '') + '$' + longP.toFixed(2);
    document.getElementById('futLongPayout').style.color = longP >= 0 ? '#10b981' : '#ef4444';
    
    document.getElementById('futShortPayout').innerText = (shortP >= 0 ? '+' : '') + '$' + shortP.toFixed(2);
    document.getElementById('futShortPayout').style.color = shortP >= 0 ? '#10b981' : '#ef4444';
}
setTimeout(calcFutApp, 500);
</script>
"""

# 3. Options Applications
pages["view-cqf-fp-deriv-options-apps.html"] = make_header("Options Applications", badge2="Derivatives") + """
    <div class="card">
        <h3>3.1 Strategic Options Applications</h3>
        <p>Unlike futures which oblige performance, options give asymmetrical **rights** to buy or sell. They are highly valued for:</p>
        <ul>
            <li><strong>Leveraged Speculation:</strong> Buying calls instead of stock to limit risk to premium while magnifying percentage upside.</li>
            <li><strong>Portfolio Insurance:</strong> Buying protective puts to lock in a floor price for stock holdings.</li>
        </ul>
        <p>A protective put portfolio payoff: $$ Y_T = S_T + \max(K - S_T, 0) - P_0 = \max(S_T, K) - P_0 $$</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Portfolio Insurance (Protective Put) Simulator</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Stock Entry Price ($S_0$):</label>
                <input id="optAppS0" type="number" value="100" style="padding: 0.4rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcOptApp()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Put Strike ($K$):</label>
                <input id="optAppK" type="number" value="95" style="padding: 0.4rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcOptApp()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Put Premium ($P_0$):</label>
                <input id="optAppP0" type="number" value="4" style="padding: 0.4rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcOptApp()">
            </div>
        </div>

        <div style="margin-bottom: 1.5rem;">
            <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Expiry Spot Price ($S_T$):</label>
            <input id="optAppST" type="range" min="60" max="140" value="80" style="width: 100%;" oninput="calcOptApp()">
            <span id="optAppSTVal" style="font-size: 0.85rem; font-weight: 700; color: var(--accent);">$80</span>
        </div>

        <div style="background: var(--metric-bg); padding: 1rem; border-radius: 8px; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="border-right: 1px solid var(--card-border); padding-right: 1rem;">
                <h4 style="margin-top: 0; color: #4f46e5;">Unhedged Stock Payoff</h4>
                <div id="optAppStockVal" style="font-size: 1.3rem; font-weight: 800; color: #ef4444;">$80.00</div>
            </div>
            <div style="padding-left: 1rem;">
                <h4 style="margin-top: 0; color: #10b981;">Protective Put Portfolio Payoff</h4>
                <div id="optAppPortVal" style="font-size: 1.3rem; font-weight: 800; color: #10b981;">$91.00</div>
            </div>
        </div>
    </div>
</div>

<script>
function calcOptApp() {
    const s0 = parseFloat(document.getElementById('optAppS0').value) || 0;
    const k = parseFloat(document.getElementById('optAppK').value) || 0;
    const p0 = parseFloat(document.getElementById('optAppP0').value) || 0;
    const st = parseFloat(document.getElementById('optAppST').value);
    
    document.getElementById('optAppSTVal').innerText = '$' + st;
    document.getElementById('optAppStockVal').innerText = '$' + st.toFixed(2);
    
    const putPayoff = Math.max(k - st, 0);
    const portPayoff = st + putPayoff - p0;
    
    document.getElementById('optAppPortVal').innerText = '$' + portPayoff.toFixed(2);
}
setTimeout(calcOptApp, 500);
</script>
"""

# 4. Fundamentals of Options
pages["view-cqf-fp-deriv-options-fundamentals.html"] = make_header("Fundamentals of Options", badge2="Derivatives") + """
    <div class="card">
        <h3>4.1 Option Contract Fundamentals</h3>
        <p>Options are standardized contracts giving holders a right (no obligation) and writers an obligation to execute:</p>
        <ul>
            <li><strong>Call Option:</strong> Right to buy at strike $K$ before expiry $T$.</li>
            <li><strong>Put Option:</strong> Right to sell at strike $K$ before expiry $T$.</li>
        </ul>
        <p>Intrinsic Payoff equations:</p>
        <p>$$ \text{Long Call: } \max(S_T - K, 0) $$</p>
        <p>$$ \text{Long Put: } \max(K - S_T, 0) $$</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Option Expiry Payoff Grapher</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Option Type:</label>
                <select id="optType" onchange="drawOptPayoff()" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;">
                    <option value="call">Call Option</option>
                    <option value="put">Put Option</option>
                </select>
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Strike ($K$):</label>
                <input id="optStrike" type="number" value="100" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 70px;" oninput="drawOptPayoff()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Premium ($C$ or $P$):</label>
                <input id="optPremium" type="number" value="5" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 70px;" oninput="drawOptPayoff()">
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border);">
            <h4 style="margin-top:0; color: var(--accent);">Live Payoff Table:</h4>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem;">
                <thead>
                    <tr style="border-bottom: 1px solid var(--card-border); text-align: left;">
                        <th style="padding: 0.4rem;">Spot Price</th>
                        <th style="padding: 0.4rem;">Gross Payoff</th>
                        <th style="padding: 0.4rem;">Net Profit/Loss</th>
                    </tr>
                </thead>
                <tbody id="optTableBody">
                </tbody>
            </table>
        </div>
    </div>
</div>

<script>
function drawOptPayoff() {
    const type = document.getElementById('optType').value;
    const strike = parseFloat(document.getElementById('optStrike').value) || 0;
    const prem = parseFloat(document.getElementById('optPremium').value) || 0;
    const tbody = document.getElementById('optTableBody');
    tbody.innerHTML = '';
    
    const spots = [strike * 0.8, strike * 0.9, strike, strike * 1.1, strike * 1.2];
    for (const s of spots) {
        const payoff = type === 'call' ? Math.max(s - strike, 0) : Math.max(strike - s, 0);
        const profit = payoff - prem;
        const color = profit >= 0 ? '#10b981' : '#ef4444';
        
        tbody.innerHTML += `
            <tr style="border-bottom: 1px solid var(--card-border);">
                <td style="padding:0.4rem;">$${s.toFixed(2)}</td>
                <td style="padding:0.4rem;">$${payoff.toFixed(2)}</td>
                <td style="padding:0.4rem; color:${color}; font-weight:700;">$${(profit >= 0 ? '+' : '')}${profit.toFixed(2)}</td>
            </tr>
        `;
    }
}
setTimeout(drawOptPayoff, 500);
</script>
"""

# 5. Interest Rate Swaps
pages["view-cqf-fp-deriv-ir-swaps.html"] = make_header("Interest Rate Swaps", badge2="Derivatives") + """
    <div class="card">
        <h3>5.1 Mechanics of Swap Contracts</h3>
        <p>Interest rate swaps (IRS) are over-the-counter agreements where parties exchange fixed rate interest payments for floating index cash flows (e.g. daily SOFR or SOFR-derived indexes):</p>
        <ul>
            <li><strong>Payer Swap:</strong> Pays fixed, receives floating. Beneficiary when interest rates rise.</li>
            <li><strong>Receiver Swap:</strong> Pays floating, receives fixed. Beneficiary when interest rates fall.</li>
        </ul>
        <p>Net cash payment for Fixed Payer at step $i$: $$ \text{Net Cash Flow} = N \times (R_{\text{floating}} - R_{\text{fixed}}) \times \Delta t $$</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Swap Cash Flow Calculator</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Notional ($N$):</label>
                <input id="swapNotional" type="number" value="1000000" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcSwap()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Fixed Rate (p.a.):</label>
                <input id="swapFixed" type="number" value="4.50" step="0.1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcSwap()"> %
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Floating Reference Rate:</label>
                <input id="swapFloat" type="number" value="5.25" step="0.1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcSwap()"> %
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border);">
            <h4 style="margin-top: 0; color: var(--accent);">Semi-Annual Coupon Net Settlement:</h4>
            <div style="font-size: 1.5rem; font-weight: 800; color: #10b981;" id="swapNetFlow">+$3,750.00</div>
            <p style="font-size: 0.85rem; margin-top: 0.5rem;" id="swapExplanation">Payer receives float, pays fixed. Net gain since Float > Fixed.</p>
        </div>
    </div>
</div>

<script>
function calcSwap() {
    const notional = parseFloat(document.getElementById('swapNotional').value) || 0;
    const fixed = (parseFloat(document.getElementById('swapFixed').value) || 0) / 100;
    const floating = (parseFloat(document.getElementById('swapFloat').value) || 0) / 100;
    
    const flow = notional * (floating - fixed) * 0.5;
    
    document.getElementById('swapNetFlow').innerText = (flow >= 0 ? '+' : '') + '$' + flow.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('swapNetFlow').style.color = flow >= 0 ? '#10b981' : '#ef4444';
    
    document.getElementById('swapExplanation').innerText = flow >= 0 
        ? "Payer Swap receives float and pays fixed, yielding a net positive incoming flow." 
        : "Payer Swap pays fixed rate exceeding float index, producing a net outgoing cash flow.";
}
setTimeout(calcSwap, 500);
</script>
"""

# 6. Introduction to Derivatives
pages["view-cqf-fp-deriv-intro.html"] = make_header("Introduction to Derivatives", badge2="Derivatives") + """
    <div class="card">
        <h3>6.1 Derivatives Taxonomy</h3>
        <p>Derivatives are bilateral agreements that derive value from an underlying reference asset (stocks, interest rates, indices). They fall into two main structures:</p>
        <ul>
            <li><strong>Exchange-Traded (ETD):</strong> Traded on standardized central exchanges with zero counterparty risk due to clearinghouses (e.g. CME).</li>
            <li><strong>Over-the-Counter (OTC):</strong> Privately negotiated, bespoke parameters and margins (e.g. most Swaps &amp; FX forwards).</li>
        </ul>
        <p>The four primary categories of derivatives are: <strong>Forwards</strong>, <strong>Futures</strong>, <strong>Options</strong>, and <strong>Swaps</strong>.</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Contract Specifications &amp; Size Sandbox</h3>
        <p>Select a contract type to see typical standard sizes, margins, and trade locations:</p>
        
        <select id="introType" onchange="updateIntroInfo()" style="padding: 0.4rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%; font-weight: 600;">
            <option value="fut_oil">Crude Oil Future (WTI)</option>
            <option value="opt_apple">Equity Option (Apple)</option>
            <option value="irs">USD Swap (OTC)</option>
        </select>
        
        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border); margin-top: 1rem; font-size: 0.9rem;" id="introDetails">
            <!-- Details generated dynamically -->
        </div>
    </div>
</div>

<script>
function updateIntroInfo() {
    const type = document.getElementById('introType').value;
    const target = document.getElementById('introDetails');
    if (type === 'fut_oil') {
        target.innerHTML = `
            <p><strong>Contract Size:</strong> 1,000 barrels</p>
            <p><strong>Exchange:</strong> NYMEX (CME Group) - Standardized</p>
            <p><strong>Initial Margin Requirement:</strong> ~$7,500 per contract</p>
            <p><strong>Clearinghouse Risk:</strong> Zero (Central Counterparty)</p>
        `;
    } else if (type === 'opt_apple') {
        target.innerHTML = `
            <p><strong>Contract Size:</strong> 100 shares of Apple stock</p>
            <p><strong>Exchange:</strong> Cboe Options Exchange - Standardized</p>
            <p><strong>Cost:</strong> Premium paid upfront</p>
            <p><strong>Default Risk:</strong> Guaranteed by OCC (Options Clearing Corp)</p>
        `;
    } else {
        target.innerHTML = `
            <p><strong>Contract Size:</strong> Custom (Bespoke Notional, e.g. $10,000,000)</p>
            <p><strong>Market:</strong> Over-the-Counter (OTC) - Bespoke</p>
            <p><strong>Collateral Structure:</strong> Credit Support Annex (CSA) under ISDA agreement</p>
            <p><strong>Default Risk:</strong> Bilateral Counterparty Credit Risk</p>
        `;
    }
}
setTimeout(updateIntroInfo, 500);
</script>
"""

# 7. Option Premiums & Valuation
pages["view-cqf-fp-deriv-options-valuation.html"] = make_header("Option Premiums & Valuation", badge2="Derivatives") + """
    <div class="card">
        <h3>7.1 Valuation of Option Premiums</h3>
        <p>An option premium comprises two distinct structural values:</p>
        <p style="text-align: center; font-size: 1.05rem; font-weight: 700;">$$ \text{Premium} = \text{Intrinsic Value} + \text{Time Value} $$</p>
        <ul>
            <li><strong>Intrinsic Value:</strong> Payoff if exercised immediately. For a Call, $\max(S - K, 0)$.</li>
            <li><strong>Time Value:</strong> Value associated with the probability of moving further in-the-money before expiry, driven by asset volatility ($\sigma$) and time to expiry ($T$).</li>
        </ul>
        <p>The Black-Scholes formula is used to value the fair premium: $$ C = S_0 N(d_1) - K e^{-r T} N(d_2) $$</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Option Premium Valuation Panel</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Spot Price ($S$):</label>
                <input id="valSpot" type="number" value="103" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 70px;" oninput="calcPremium()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Strike ($K$):</label>
                <input id="valStrike" type="number" value="100" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 70px;" oninput="calcPremium()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Total Premium:</label>
                <input id="valPremium" type="number" value="7.50" step="0.5" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 70px;" oninput="calcPremium()">
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border); display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="border-right: 1px solid var(--card-border); padding-right: 1rem;">
                <h4 style="margin-top: 0; color: #4f46e5;">Intrinsic Value</h4>
                <div id="valIntrinsic" style="font-size: 1.5rem; font-weight: 800; color: #10b981;">$3.00</div>
            </div>
            <div style="padding-left: 1rem;">
                <h4 style="margin-top: 0; color: #0ea5e9;">Time Value</h4>
                <div id="valTime" style="font-size: 1.5rem; font-weight: 800; color: #0ea5e9;">$4.50</div>
            </div>
        </div>
    </div>
</div>

<script>
function calcPremium() {
    const s = parseFloat(document.getElementById('valSpot').value) || 0;
    const k = parseFloat(document.getElementById('valStrike').value) || 0;
    const prem = parseFloat(document.getElementById('valPremium').value) || 0;
    
    const intrinsic = Math.max(s - k, 0);
    const timeVal = Math.max(prem - intrinsic, 0);
    
    document.getElementById('valIntrinsic').innerText = '$' + intrinsic.toFixed(2);
    document.getElementById('valTime').innerText = '$' + timeVal.toFixed(2);
}
setTimeout(calcPremium, 500);
</script>
"""

# 8. Futures & Forwards Fundamentals
pages["view-cqf-fp-deriv-futures-fundamentals.html"] = make_header("Futures & Forwards Fundamentals", badge2="Derivatives") + """
    <div class="card">
        <h3>8.1 Performance Margining &amp; Obligation</h3>
        <p>Futures and forwards both represent binding obligations to buy or sell. However, futures employ a daily exchange margining process to fully neutralize default risk:</p>
        <ul>
            <li><strong>Initial Margin:</strong> The deposit required per contract to enter the trade.</li>
            <li><strong>Maintenance Margin:</strong> The absolute lower limit below which a margin call is triggered, forcing immediate top-ups.</li>
        </ul>
        <p>Daily gains/losses are marked-to-market daily and transferred directly into/out of margin accounts.</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Futures Margin &amp; Leverage Calculator</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Contract Notional ($):</label>
                <input id="margNotional" type="number" value="60000" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcMargin()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Initial Margin ($):</label>
                <input id="margInit" type="number" value="3000" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcMargin()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Maintenance Limit ($):</label>
                <input id="margMaint" type="number" value="2200" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcMargin()">
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border); display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="border-right: 1px solid var(--card-border); padding-right: 1rem;">
                <h4 style="margin-top: 0; color: #4f46e5;">Leverage Ratio</h4>
                <div id="margLeverage" style="font-size: 1.5rem; font-weight: 800; color: #4f46e5;">20.0x</div>
            </div>
            <div style="padding-left: 1rem;">
                <h4 style="margin-top: 0; color: #ef4444;">Maximum Loss Allowed</h4>
                <div id="margMaxLoss" style="font-size: 1.5rem; font-weight: 800; color: #ef4444;">$800.00</div>
            </div>
        </div>
    </div>
</div>

<script>
function calcMargin() {
    const notional = parseFloat(document.getElementById('margNotional').value) || 1;
    const init = parseFloat(document.getElementById('margInit').value) || 1;
    const maint = parseFloat(document.getElementById('margMaint').value) || 0;
    
    const leverage = notional / init;
    const maxLoss = init - maint;
    
    document.getElementById('margLeverage').innerText = leverage.toFixed(1) + 'x';
    document.getElementById('margMaxLoss').innerText = '$' + maxLoss.toFixed(2);
}
setTimeout(calcMargin, 500);
</script>
"""

# 9. Futures & Forwards Valuation
pages["view-cqf-fp-deriv-futures-valuation.html"] = make_header("Futures & Forwards Valuation", badge2="Derivatives") + """
    <div class="card">
        <h3>9.1 Spot-Forward Valuation &amp; Cost of Carry</h3>
        <p>The fair theoretical futures price is determined purely by arbitrage replication: the spot purchase plus carrying costs to the maturity date. This is the **Cost of Carry** model:</p>
        <p style="text-align: center; font-size: 1.15rem; font-weight: 700;">$$ F_0 = S_0 e^{(r + u - q)T} $$</p>
        <ul>
            <li>$r$: continuous risk-free rate of return.</li>
            <li>$u$: continuous storage/insurance costs.</li>
            <li>$q$: continuous dividend yield or convenience yield.</li>
        </ul>
        <p>If $F_{\text{market}} > F_{\text{theoretical}}$, an arbitrageur can borrow money, buy spot, and sell futures to lock in a risk-free return.</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Cost-of-Carry Arbitrage Calculator</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Spot Price ($S_0$):</label>
                <input id="carrySpot" type="number" value="100" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcCarry()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Risk-free ($r$, p.a.):</label>
                <input id="carryR" type="number" value="5.00" step="0.1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcCarry()"> %
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Div/Yield ($q$, p.a.):</label>
                <input id="carryQ" type="number" value="2.00" step="0.1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcCarry()"> %
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border);">
            <h4 style="margin-top: 0; color: var(--accent);">Theoretical 1-Year Forward Price:</h4>
            <div id="carryForward" style="font-size: 1.6rem; font-weight: 800; color: #10b981;">$103.05</div>
            <p style="font-size: 0.85rem; margin-top: 0.5rem;">Based on continuous replication: $100 \times e^{(0.05 - 0.02) \times 1.0}$</p>
        </div>
    </div>
</div>

<script>
function calcCarry() {
    const s0 = parseFloat(document.getElementById('carrySpot').value) || 0;
    const r = (parseFloat(document.getElementById('carryR').value) || 0) / 100;
    const q = (parseFloat(document.getElementById('carryQ').value) || 0) / 100;
    
    const f = s0 * Math.exp((r - q) * 1.0);
    document.getElementById('carryForward').innerText = '$' + f.toFixed(2);
}
setTimeout(calcCarry, 500);
</script>
"""

# 10. Financial Services & Markets
pages["view-cqf-fp-funds-markets.html"] = make_header("Financial Services & Markets", badge2="Fundamentals") + """
    <div class="card">
        <h3>10.1 Financial Markets Taxonomy</h3>
        <p>The financial services industry acts as a crucial capital conduit, connecting borrowing demands with investment allocations. Markets are structurally classified into:</p>
        <ul>
            <li><strong>Primary Markets:</strong> Where corporations raise fresh capital by issuing new securities (e.g. IPOs or fresh debt).</li>
            <li><strong>Secondary Markets:</strong> Where existing securities are traded among investors (e.g., NYSE, Nasdaq), providing crucial liquidity.</li>
        </ul>
        <p>Standard intermediaries include <strong>Investment Banks</strong> (underwriting, advisory) and <strong>Broker-Dealers</strong> (trading liquidity).</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Financial Intermediary Flow Laboratory</h3>
        <p>Select a participant to understand their structural function and capital flow direction:</p>
        
        <select id="marketFlowSelect" onchange="calcMarketFlow()" style="padding: 0.4rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%; font-weight: 600;">
            <option value="borrower">Corporation (Borrower/Issuer)</option>
            <option value="bank">Investment Bank (Intermediary)</option>
            <option value="investor">Asset Manager (Investor/Capital Supplier)</option>
        </select>
        
        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border); margin-top: 1rem; font-size: 0.95rem; line-height: 1.6;" id="marketFlowDetails">
            <!-- Details generated dynamically -->
        </div>
    </div>
</div>

<script>
function calcMarketFlow() {
    const val = document.getElementById('marketFlowSelect').value;
    const target = document.getElementById('marketFlowDetails');
    if (val === 'borrower') {
        target.innerHTML = `
            <p><strong>Primary Function:</strong> Issue shares or corporate bonds to fund capital expenditures.</p>
            <p><strong>Capital Direction:</strong> Receives cash flows from primary markets, pays coupons/dividends back to markets.</p>
            <p><strong>Regulator Supervision:</strong> SEC / FCA disclosure oversight.</p>
        `;
    } else if (val === 'bank') {
        target.innerHTML = `
            <p><strong>Primary Function:</strong> Act as underwriter to advise on pricing, credit rating spreads, and distribute bonds/equity.</p>
            <p><strong>Capital Direction:</strong> Facilitator. Charges advisory and underwriting fees (gross spread).</p>
            <p><strong>Market Impact:</strong> Enhances pricing efficiency and corporate outreach.</p>
        `;
    } else {
        target.innerHTML = `
            <p><strong>Primary Function:</strong> Allocate client funds into fixed-income or equity securities to generate target returns.</p>
            <p><strong>Capital Direction:</strong> Capital supplier. Provides liquidity to secondary markets and subscribes in primary markets.</p>
            <p><strong>Oversight focus:</strong> Fiduciary duty and compliance mandates.</p>
        `;
    }
}
setTimeout(calcMarketFlow, 500);
</script>
"""

# 11. Central Banks & Reference Rates
pages["view-cqf-fp-funds-rates.html"] = make_header("Central Banks & Reference Rates", badge2="Fundamentals") + """
    <div class="card">
        <h3>11.1 Central Bank Policy &amp; Overnight Indices</h3>
        <p>Central banks target specific short-term reference rates to manage inflation and monetary policy transmission. In modern overnight markets, standardized backward-looking compounding rates have fully replaced LIBOR:</p>
        <ul>
            <li><strong>SOFR (Secured Overnight Financing Rate):</strong> Compounded secured Treasury repo index.</li>
            <li><strong>SONIA (Sterling Overnight Index Average):</strong> British overnight interbank lending index.</li>
        </ul>
        <p>The daily compounding of overnight index rates over accrual periods: $$ R_{\text{comp}} = \left( \prod_{i=1}^{d_c} \left(1 + \frac{r_i \Delta t_i}{360}\right) - 1 \right) \times \frac{360}{d} $$</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Overnight Index Compounding Simulator</h3>
        <p>Simulate five consecutive business days of fluctuating overnight rates and see the final backward-looking compounded reference rate:</p>
        
        <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.5rem; margin-bottom: 1.5rem;">
            <div><label style="font-size:0.75rem; font-weight:600;">Day 1:</label><input id="rRate1" type="number" value="5.25" step="0.05" style="width: 100%; padding:0.2rem;" oninput="calcRatesComp()"></div>
            <div><label style="font-size:0.75rem; font-weight:600;">Day 2:</label><input id="rRate2" type="number" value="5.30" step="0.05" style="width: 100%; padding:0.2rem;" oninput="calcRatesComp()"></div>
            <div><label style="font-size:0.75rem; font-weight:600;">Day 3:</label><input id="rRate3" type="number" value="5.28" step="0.05" style="width: 100%; padding:0.2rem;" oninput="calcRatesComp()"></div>
            <div><label style="font-size:0.75rem; font-weight:600;">Day 4:</label><input id="rRate4" type="number" value="5.25" step="0.05" style="width: 100%; padding:0.2rem;" oninput="calcRatesComp()"></div>
            <div><label style="font-size:0.75rem; font-weight:600;">Day 5:</label><input id="rRate5" type="number" value="5.32" step="0.05" style="width: 100%; padding:0.2rem;" oninput="calcRatesComp()"></div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border);">
            <h4 style="margin-top: 0; color: var(--accent);">Compounded Reference Rate (5-Day Period):</h4>
            <div id="rateCompResult" style="font-size: 1.6rem; font-weight: 800; color: #4f46e5;">5.281%</div>
        </div>
    </div>
</div>

<script>
function calcRatesComp() {
    let rates = [];
    for(let i=1; i<=5; i++) {
        rates.push((parseFloat(document.getElementById('rRate' + i).value) || 0) / 100);
    }
    
    let compound = 1.0;
    const dt = 1 / 360;
    for(const r of rates) {
        compound *= (1 + r * dt);
    }
    
    const finalRate = (compound - 1) * (360 / 5) * 100;
    document.getElementById('rateCompResult').innerText = finalRate.toFixed(4) + '%';
}
setTimeout(calcRatesComp, 500);
</script>
"""

# 12. Basics of Macro Economics
pages["view-cqf-fp-funds-macro.html"] = make_header("Basics of Macroeconomics", badge2="Fundamentals") + """
    <div class="card">
        <h3>12.1 Macroeconomic Equilibrium</h3>
        <p>Macroeconomics studies broad economic aggregates. Central banks balance growth and price stability using the **Taylor Rule** reference framework:</p>
        <ul>
            <li><strong>GDP (Gross Domestic Product):</strong> Measures absolute economic growth and aggregate output.</li>
            <li><strong>Inflation Target:</strong> Maintaining price stability (usually targeted around 2% p.a.).</li>
        </ul>
        <p>Simplified Taylor Rule for policy interest rates: $$ i_t = r^* + \pi_t + 0.5(\pi_t - \pi^*) + 0.5(y_t - y^*) $$</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Taylor Rule Monetary Policy Sandbox</h3>
        <p>Adjust current inflation and the output gap (GDP deviation) to see the central bank's suggested policy interest rate:</p>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Current Inflation ($\pi_t$):</label>
                <input id="macroInf" type="range" min="-1" max="8" step="0.1" value="3.5" oninput="calcMacro()" style="width: 100%;">
                <span id="macroInfVal" style="font-size: 0.85rem; font-weight: 700; color: var(--accent);">3.5%</span>
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Output Gap ($y_t - y^*$):</label>
                <input id="macroGap" type="range" min="-3" max="3" step="0.1" value="1.0" oninput="calcMacro()" style="width: 100%;">
                <span id="macroGapVal" style="font-size: 0.85rem; font-weight: 700; color: var(--accent);">+1.0%</span>
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border);">
            <h4 style="margin-top: 0; color: var(--accent);">Target Policy Interest Rate:</h4>
            <div id="macroResult" style="font-size: 1.6rem; font-weight: 800; color: #ef4444;">6.25%</div>
            <p style="font-size: 0.85rem; margin-top: 0.5rem;" id="macroExplanation">Suggests rate hikes to cool down inflation above target.</p>
        </div>
    </div>
</div>

<script>
function calcMacro() {
    const pi_t = parseFloat(document.getElementById('macroInf').value);
    const gap = parseFloat(document.getElementById('macroGap').value);
    
    document.getElementById('macroInfVal').innerText = pi_t.toFixed(1) + '%';
    document.getElementById('macroGapVal').innerText = (gap >= 0 ? '+' : '') + gap.toFixed(1) + '%';
    
    const r_star = 2.0; // neutral real rate
    const pi_star = 2.0; // inflation target
    
    const policy = r_star + pi_t + 0.5 * (pi_t - pi_star) + 0.5 * gap;
    
    document.getElementById('macroResult').innerText = policy.toFixed(2) + '%';
    
    if (pi_t > pi_star) {
        document.getElementById('macroExplanation').innerText = "Suggested policy stance: Contractionary (Rate Hike) to curb inflationary pressures.";
        document.getElementById('macroResult').style.color = '#ef4444';
    } else {
        document.getElementById('macroExplanation').innerText = "Suggested policy stance: Accommodative / Neutral (Lower Rates) to stimulate growth.";
        document.getElementById('macroResult').style.color = '#10b981';
    }
}
setTimeout(calcMacro, 500);
</script>
"""

# 13. Basic Forward FX
pages["view-cqf-fp-fx-forward.html"] = make_header("Basic Forward FX Outrights", badge2="Foreign Exchange") + """
    <div class="card">
        <h3>13.1 FX Outright Forward Parity</h3>
        <p>In currency markets, outright forward transactions agree currencies swap terms at non-spot future dates. The forward rate is driven by the **Interest Rate Parity** arbitrage relation:</p>
        <p style="text-align: center; font-size: 1.15rem; font-weight: 700;">$$ F_0 = S_0 \times \frac{1 + r_d T}{1 + r_f T} $$</p>
        <ul>
            <li>$S_0$: Current Spot Rate (Domestic/Foreign ratio).</li>
            <li>$r_d$: Domestic reference interest rate (base currency side).</li>
            <li>$r_f$: Foreign reference interest rate (quote currency side).</li>
        </ul>
        <p>The difference $F_0 - S_0$ is defined as the **Forward Points** spread.</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Outright Forward FX Parity Calculator</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Spot EUR/USD ($S_0$):</label>
                <input id="fxSpot" type="number" value="1.1000" step="0.001" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcFXFwd()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">USD Rate ($r_d$, p.a.):</label>
                <input id="fxRD" type="number" value="5.00" step="0.1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcFXFwd()"> %
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">EUR Rate ($r_f$, p.a.):</label>
                <input id="fxRF" type="number" value="3.00" step="0.1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcFXFwd()"> %
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border); display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="border-right: 1px solid var(--card-border); padding-right: 1rem;">
                <h4 style="margin-top: 0; color: #4f46e5;">1-Year Forward Rate</h4>
                <div id="fxFwdRate" style="font-size: 1.5rem; font-weight: 800; color: #4f46e5;">1.1214</div>
            </div>
            <div style="padding-left: 1rem;">
                <h4 style="margin-top: 0; color: #10b981;">Forward Points</h4>
                <div id="fxFwdPoints" style="font-size: 1.5rem; font-weight: 800; color: #10b981;">+214</div>
            </div>
        </div>
    </div>
</div>

<script>
function calcFXFwd() {
    const s0 = parseFloat(document.getElementById('fxSpot').value) || 0;
    const rd = (parseFloat(document.getElementById('fxRD').value) || 0) / 100;
    const rf = (parseFloat(document.getElementById('fxRF').value) || 0) / 100;
    
    const f = s0 * ((1 + rd * 1.0) / (1 + rf * 1.0));
    const points = (f - s0) * 10000;
    
    document.getElementById('fxFwdRate').innerText = f.toFixed(4);
    document.getElementById('fxFwdPoints').innerText = (points >= 0 ? '+' : '') + Math.round(points);
}
setTimeout(calcFXFwd, 500);
</script>
"""

# 14. FX Basics
pages["view-cqf-fp-fx-basics.html"] = make_header("FX Basics", badge2="Foreign Exchange") + """
    <div class="card">
        <h3>14.1 Foreign Exchange Structure</h3>
        <p>Currencies are traded strictly in pairs (e.g. EUR/USD). The US Dollar acts as the global primary reserve currency, participating in the vast majority of trades.</p>
        <p>Terminology: <strong>Base Currency</strong> / <strong>Quote Currency</strong>.</p>
        <p>For a quote pair $C_1 / C_2 = X$, $1$ unit of base currency $C_1$ buys $X$ units of quote currency $C_2$.</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Cross-Rate Converter Matrix</h3>
        <p>Convert EUR and GBP to USD simultaneously based on current live rates:</p>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">EUR/USD Spot Rate:</label>
                <input id="fxBasEur" type="number" value="1.0950" step="0.0005" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcFXBas()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">GBP/USD Spot Rate:</label>
                <input id="fxBasGbp" type="number" value="1.2750" step="0.0005" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcFXBas()">
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border);">
            <h4 style="margin-top:0; color:var(--accent);">Derived EUR/GBP Cross-Rate:</h4>
            <div id="fxBasCross" style="font-size: 1.6rem; font-weight: 800; color: #4f46e5;">0.8588</div>
            <p style="font-size:0.85rem; margin-top:0.5rem;">Calculated via: (EUR/USD) / (GBP/USD)</p>
        </div>
    </div>
</div>

<script>
function calcFXBas() {
    const eur = parseFloat(document.getElementById('fxBasEur').value) || 0.0001;
    const gbp = parseFloat(document.getElementById('fxBasGbp').value) || 0.0001;
    
    const cross = eur / gbp;
    document.getElementById('fxBasCross').innerText = cross.toFixed(4);
}
setTimeout(calcFXBas, 500);
</script>
"""

# 15. Corporate Bonds
pages["view-cqf-fp-sec-corp-bonds.html"] = make_header("Corporate Bonds", badge2="Securities") + """
    <div class="card">
        <h3>15.1 Corporate Debt &amp; Credit Spread</h3>
        <p>Large corporations issue corporate bonds to secure capital. Unlike default-free government debt, corporate yields feature a structural **Credit Spread** premium:</p>
        <p style="text-align: center; font-size: 1.1rem; font-weight: 700;">$$ \text{Corporate Yield} = \text{Treasury Yield} + \text{Credit Spread} $$</p>
        <ul>
            <li><strong>Credit Rating:</strong> Evaluated by Standard &amp; Poor's, Moody's, or Fitch (AAA down to D) representing default probability.</li>
            <li><strong>Spread:</strong> Additional basis point spread required by bondholders to absorb credit risk.</li>
        </ul>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Credit Spread &amp; Corporate Yield Solver</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Benchmark Treasury Yield:</label>
                <input id="corpTreas" type="number" value="4.25" step="0.05" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcCorpBond()"> %
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Credit Rating Tier:</label>
                <select id="corpRating" onchange="calcCorpBond()" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;">
                    <option value="50">AAA (spread: 50 bps)</option>
                    <option value="120">BBB (spread: 120 bps)</option>
                    <option value="350">BB (spread: 350 bps)</option>
                    <option value="750">CCC (spread: 750 bps)</option>
                </select>
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border); display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div style="border-right: 1px solid var(--card-border); padding-right: 1rem;">
                <h4 style="margin-top: 0; color: #4f46e5;">Credit Spread (bps)</h4>
                <div id="corpSpreadVal" style="font-size: 1.5rem; font-weight: 800; color: #4f46e5;">120 bps</div>
            </div>
            <div style="padding-left: 1rem;">
                <h4 style="margin-top: 0; color: #10b981;">Total Corporate Yield</h4>
                <div id="corpTotalYield" style="font-size: 1.5rem; font-weight: 800; color: #10b981;">5.45%</div>
            </div>
        </div>
    </div>
</div>

<script>
function calcCorpBond() {
    const treas = parseFloat(document.getElementById('corpTreas').value) || 0;
    const spreadBps = parseInt(document.getElementById('corpRating').value);
    
    const spreadPct = spreadBps / 10000;
    const totalYield = treas + (spreadPct * 100);
    
    document.getElementById('corpSpreadVal').innerText = spreadBps + ' bps';
    document.getElementById('corpTotalYield').innerText = totalYield.toFixed(2) + '%';
}
setTimeout(calcCorpBond, 500);
</script>
"""

# 16. Equities
pages["view-cqf-fp-sec-equities.html"] = make_header("Equities Valuation", badge2="Securities") + """
    <div class="card">
        <h3>16.1 Dividend Discount Model (DDM)</h3>
        <p>Common shares yield fractional ownership and dividend rights. Under the classic **Gordon Growth Model**, equity value is the present value of all future growing dividends:</p>
        <p style="text-align: center; font-size: 1.15rem; font-weight: 700;">$$ V_0 = \frac{D_0 (1 + g)}{r - g} $$</p>
        <ul>
            <li>$D_0$: Current dividend payout.</li>
            <li>$g$: Constant growth rate of dividends.</li>
            <li>$r$: Investors' required rate of return ($r > g$).</li>
        </ul>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Gordon Growth Equities Valuation Panel</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Dividend ($D_0$):</label>
                <input id="eqDiv" type="number" value="2.50" step="0.10" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcEquity()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Required Return ($r$, p.a.):</label>
                <input id="eqR" type="number" value="8.00" step="0.1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcEquity()"> %
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Growth Rate ($g$, p.a.):</label>
                <input id="eqG" type="number" value="3.00" step="0.1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcEquity()"> %
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border);">
            <h4 style="margin-top: 0; color: var(--accent);">Derived Intrinsic Share Value:</h4>
            <div id="eqShareValue" style="font-size: 1.6rem; font-weight: 800; color: #10b981;">$51.50</div>
        </div>
    </div>
</div>

<script>
function calcEquity() {
    const d0 = parseFloat(document.getElementById('eqDiv').value) || 0;
    const r = (parseFloat(document.getElementById('eqR').value) || 0) / 100;
    const g = (parseFloat(document.getElementById('eqG').value) || 0) / 100;
    
    if (r <= g) {
        document.getElementById('eqShareValue').innerHTML = '<span style="color:#ef4444; font-size:1.1rem;">Required rate $r$ must be greater than growth rate $g$</span>';
        return;
    }
    
    const v = (d0 * (1 + g)) / (r - g);
    document.getElementById('eqShareValue').innerText = '$' + v.toFixed(2);
}
setTimeout(calcEquity, 500);
</script>
"""

# 17. Gov Bills, Notes & Bonds
pages["view-cqf-fp-sec-gov-securities.html"] = make_header("Government Bills, Notes & Bonds", badge2="Securities") + """
    <div class="card">
        <h3>17.1 Sovereign Debt Instruments</h3>
        <p>Governments borrow money across varying maturities to fund balance deficits. Key sovereign instruments include:</p>
        <ul>
            <li><strong>Bills (T-Bills):</strong> Short-term zero-coupon securities (maturing under 1 year) traded at a discount.</li>
            <li><strong>Notes/Bonds:</strong> Coupon-bearing securities maturing in 2 to 30 years.</li>
        </ul>
        <p>Pricing equation for sovereign coupon bond: $$ P_0 = \sum_{t=1}^{T} \frac{C}{(1+y)^t} + \frac{F}{(1+y)^T} $$</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Bond Yield-Price Sensitivity Laboratory</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Coupon Rate (p.a.):</label>
                <input id="govC" type="number" value="4.00" step="0.1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcGovBond()"> %
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Maturity ($T$ Years):</label>
                <input id="govT" type="number" value="10" step="1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcGovBond()"> years
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Yield-to-Maturity ($y$):</label>
                <input id="govY" type="number" value="4.50" step="0.1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcGovBond()"> %
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border);">
            <h4 style="margin-top: 0; color: var(--accent);">Derived Bond Price (per $100 Par):</h4>
            <div id="govPriceResult" style="font-size: 1.6rem; font-weight: 800; color: #ef4444;">$96.04</div>
        </div>
    </div>
</div>

<script>
function calcGovBond() {
    const c = (parseFloat(document.getElementById('govC').value) || 0) / 100;
    const t = parseInt(document.getElementById('govT').value) || 1;
    const y = (parseFloat(document.getElementById('govY').value) || 0) / 100;
    
    let price = 0;
    const coupon = 100 * c;
    for(let i=1; i<=t; i++) {
        price += coupon / Math.pow(1 + y, i);
    }
    price += 100 / Math.pow(1 + y, t);
    
    document.getElementById('govPriceResult').innerText = '$' + price.toFixed(2);
    document.getElementById('govPriceResult').style.color = price >= 100 ? '#10b981' : '#ef4444';
}
setTimeout(calcGovBond, 500);
</script>
"""

# 18. Time Value of Money - Compounding
pages["view-cqf-fp-tvm-compounding.html"] = make_header("Compounding & Future Values", badge2="Time Value of Money") + """
    <div class="card">
        <h3>18.1 Time Value of Money &amp; Compounding</h3>
        <p>A dollar today is worth more than a dollar tomorrow due to interest-earning potential. Future Value represents growing present cash flows over time:</p>
        <p>Standard discrete compounding ($m$ times a year): $$ FV = PV \left(1 + \frac{r}{m}\right)^{m T} $$</p>
        <p>Continuous compounding ($m \to \infty$): $$ FV = PV e^{r T} $$</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Future Value Compounding Calculator</h3>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Present Value ($PV$):</label>
                <input id="tvmPV" type="number" value="1000" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcTVMFV()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Interest Rate ($r$, p.a.):</label>
                <input id="tvmR" type="number" value="6.00" step="0.1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 80px;" oninput="calcTVMFV()"> %
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Years ($T$):</label>
                <input id="tvmT" type="number" value="5" step="1" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 60px;" oninput="calcTVMFV()"> years
            </div>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border); font-size: 0.95rem;">
            <h4 style="margin-top: 0; color: var(--accent);">Future Value under different frequencies:</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; line-height: 1.6;">
                <div>Annual: <strong id="fvAnn" style="color: #4f46e5;">$1,338.23</strong></div>
                <div>Semi-Annual: <strong id="fvSemi" style="color: #4f46e5;">$1,343.92</strong></div>
                <div>Monthly: <strong id="fvMonth" style="color: #4f46e5;">$1,348.85</strong></div>
                <div>Continuous: <strong id="fvCont" style="color: #10b981;">$1,349.86</strong></div>
            </div>
        </div>
    </div>
</div>

<script>
function calcTVMFV() {
    const pv = parseFloat(document.getElementById('tvmPV').value) || 0;
    const r = (parseFloat(document.getElementById('tvmR').value) || 0) / 100;
    const t = parseFloat(document.getElementById('tvmT').value) || 0;
    
    const fAnn = pv * Math.pow(1 + r/1, 1*t);
    const fSemi = pv * Math.pow(1 + r/2, 2*t);
    const fMonth = pv * Math.pow(1 + r/12, 12*t);
    const fCont = pv * Math.exp(r * t);
    
    document.getElementById('fvAnn').innerText = '$' + fAnn.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('fvSemi').innerText = '$' + fSemi.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('fvMonth').innerText = '$' + fMonth.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('fvCont').innerText = '$' + fCont.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}
setTimeout(calcTVMFV, 500);
</script>
"""

# 19. Time Value of Money - Discounting
pages["view-cqf-fp-tvm-discounting.html"] = make_header("Discounting & Present Values", badge2="Time Value of Money") + """
    <div class="card">
        <h3>19.1 Discounting &amp; Present Value (PV)</h3>
        <p>Discounting compiles future cash payouts into their present-value equivalent. It serves as the mathematical foundation for Net Present Value (NPV):</p>
        <p>Continuous discounting of cash flows $C_t$: $$ PV = \sum_{t} C_t e^{-r t} $$</p>
    </div>

    <div class="card" style="border-left: 4px solid var(--accent);">
        <h3>Interactive Present Value (PV) &amp; NPV Solver</h3>
        <p>Compiles three annual cash flows back to Year 0 using an adjustable discount rate:</p>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem;">
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Year 1 Flow:</label>
                <input id="flow1" type="number" value="200" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcTVMPV()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Year 2 Flow:</label>
                <input id="flow2" type="number" value="300" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcTVMPV()">
            </div>
            <div>
                <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Year 3 Flow:</label>
                <input id="flow3" type="number" value="500" style="padding: 0.3rem; border-radius: 6px; border: 1px solid var(--input-border); width: 100%;" oninput="calcTVMPV()">
            </div>
        </div>

        <div style="margin-bottom: 1.5rem;">
            <label style="font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Continuous Discount Rate ($r$, p.a.):</label>
            <input id="discountR" type="range" min="1" max="15" step="0.5" value="6.0" oninput="calcTVMPV()" style="width: 100%;">
            <span id="discountRVal" style="font-size: 0.85rem; font-weight: 700; color: var(--accent);">6.0%</span>
        </div>

        <div style="background: var(--metric-bg); padding: 1.25rem; border-radius: 8px; border: 1px solid var(--card-border);">
            <h4 style="margin-top: 0; color: var(--accent);">Derived Combined Present Value (PV):</h4>
            <div id="pvCombinedResult" style="font-size: 1.6rem; font-weight: 800; color: #10b981;">$857.48</div>
        </div>
    </div>
</div>

<script>
function calcTVMPV() {
    const c1 = parseFloat(document.getElementById('flow1').value) || 0;
    const c2 = parseFloat(document.getElementById('flow2').value) || 0;
    const c3 = parseFloat(document.getElementById('flow3').value) || 0;
    const r = parseFloat(document.getElementById('discountR').value) / 100;
    
    document.getElementById('discountRVal').innerText = (r * 100).toFixed(1) + '%';
    
    const pv = c1 * Math.exp(-r * 1.0) + c2 * Math.exp(-r * 2.0) + c3 * Math.exp(-r * 3.0);
    
    document.getElementById('pvCombinedResult').innerText = '$' + pv.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}
setTimeout(calcTVMPV, 500);
</script>
"""

# Write templates to files
for name, content in pages.items():
    path = os.path.join(output_dir, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated: {path}")
