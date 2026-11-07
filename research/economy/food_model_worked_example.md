# The food model, worked example (specification version 4, M101)

City E: $N=100{,}000$; $\mathbf w=(0.2,\,0.4,\,0.4)$ for vigorous, active and sedentary work. Values are computed by `plan/tools/food_model.py` from the data files and rounded for display.

## Availability (1) and the per-good data (section 3a)

| $g$ | $S_g$ [t] | $a_g$ [g/(p·d)] | $u_g$ | $e_g$ [kcal/g] | $p_g$ [g/g] | $f_g$ [g/g] | $\sigma_g$ | in $\mathcal W$ |
|---|---|---|---|---|---|---|---|---|
| Cow | 20,000 | 547.9 | 547.9 | 1.500 | 0.185 | 0.079 | 1.76 | yes |
| Dairy | 150,000 | 4,109.6 | 3,000 | 0.610 | 0.033 | 0.033 | 0.78 | yes |
| Potato | 60,000 | 1,643.8 | 1,643.8 | 0.670 | 0.016 | 0.001 | 3.23 | no |
| Wheat | 40,000 | 1,095.9 | 1,095.9 | 2.672 | 0.098 | 0.018 | 1.57 | no |
| Apple | 20,000 | 547.9 | 547.9 | 0.480 | 0.001 | 0.003 | 1.97 | yes |
| Sugar | 8,000 | 219.2 | 219.2 | 3.730 | 0 | 0 | 1.00 | yes |
| Wine | 15,000 | 411.0 | 411.0 | 0.680 | 0 | 0 | 0.70 | yes |
| Tea | 400 | 11.0 | – | – | – | – | – | stage 0 |
| Salt | 500 | 13.7 | 13.7 | 0 | 0 | 0 | – | no |

## Stage 0 and the needs, (2)-(4)

$$
\begin{aligned}
&q_{\mathrm{tea}}=\min(11.0,\ 600/8.6)=11.0\ \text{g};\qquad c=11.0\cdot8.6/600=0.157\\
&E^{\mathrm{need}}=1536\,(0.2\cdot2.25+0.4\cdot1.76+0.4\cdot1.53)+150\cdot0.157=1536\cdot1.766+23.6=2{,}735\ \text{kcal}\\
&E^{\max}=1536\cdot2.40+23.6=3{,}709\ \text{kcal}\\
&r_{\mathrm{fullness}}=1.36\cdot2{,}735=3{,}720;\qquad F^{\max}=1.36\cdot3{,}709=5{,}044;\qquad P^{\max}=228\ \text{g}
\end{aligned}
$$

## The program (10)-(12)

| Stage | Objective | Optimum |
|---|---|---|
| 1 | $\max A$ | $A^*=1.000$: all 15 components reach their need |
| 2 | $\max\Psi$ with $A\ge1$ | $\Psi^*=9.65$; the energy ceiling $E^{\max}$ binds |
| 3 | $\min\sum_gq_g/a_g$ with $A\ge1,\ \Psi\ge9.65$ | the diet below |

| $g$ | $q^*_g$ [g/(p·d)] | $e_gq^*_g$ [kcal] | $\ln(1+e_gq^*_g/100)$ | $\lambda^{(2)}_g$ [well-being per kg] |
|---|---|---|---|---|
| Cow | 547.9 (whole stock) | 822 | 2.22 | 0.76 |
| Dairy | 2,146.0 | 1,309 | 2.65 | 0 |
| Potato | 351.3 | 235 | – (staple) | 0 |
| Wheat | 0 | 0 | – (staple) | 0 |
| Apple | 547.9 (whole stock) | 263 | 1.29 | 1.01 |
| Sugar | 214.5 | 800 | 2.20 | 0 |
| Wine | 411.0 (whole stock) | 279 | 1.33 | 1.14 |
| **Σ** | | **3,709** $=E^{\max}$ | **9.69** (the linear program's piecewise value: 9.65 $=\Psi^*$) | |

**How the program reads:**
- **Stage 1** needs only part of these goods to reach $A=1$.
- **Stage 2** then spends the remaining room up to $E^{\max}$ on the goods in $\mathcal W$. Because of the logarithm, it spreads the room across all of them; beef, apples and wine run out of stock.
- **The positive $\lambda^{(2)}$:** for these three goods, more stock would raise well-being.
- **Potatoes** (351 g) are needed only to keep fullness at its need while the energy room goes to well-being goods. Wheat is not needed.
- **Stage-1 shadow values** are 0 for every good: no stock limits nutrition here.

## Outcomes (13)-(17)

$$
\begin{aligned}
(13)\quad & x=3{,}709/2{,}735=1.36;\qquad \textit{fed}=4{,}735/3{,}720=1.27;\qquad A^*=1;\qquad \Psi^*=9.65\\
(14)\quad & \textit{harm}_{\mathrm{alcohol}}=411.0\cdot0.106=43.6\ \text{g alcohol}/(\text{p·d})\\
(15)\quad & W^{\mathrm{in}}=\underbrace{1{,}058}_{\text{food water}}+\underbrace{2{,}146\cdot1.5}_{\text{milk}}+\underbrace{411\cdot1.0}_{\text{wine}}+\underbrace{11.0\cdot43}_{\text{tea}}=5{,}159\ \text{ml};\qquad W^{\mathrm{plain}}=0\\
(16)\quad & \textit{work}=\min(1,\,1.36)=1
\end{aligned}
$$

**Coverage $c_i$:**

| fullness | energy | protein | C | A | B1 | B3 | folate | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1.27 | 1.36 | 3.89 | 1.10 | 3.19 | 2.52 | 2.11 | 1.00 | 8.40 | 2.65 | 3.18 | 3.64 | 2.31 | 2.02 | 2.25 |

**Stocks (17), in tonnes:**

| $g$ | Cow | Dairy | Potato | Wheat | Apple | Sugar | Wine | Salt |
|---|---|---|---|---|---|---|---|---|
| $U_g$ | 20,000 | 78,328 | 12,823 | 0 | 20,000 | 7,828 | 15,000 | 0 |
| $L_g$ | 0 | 71,672 | 47,177 | 40,000 | 0 | 172 | 0 | 500 |
| $D_g$ | 0 | 71,672 | 23,588 | 2,000 | 0 | 17 | 0 | 50 |

## Points for decision

1. **Harmful and sweet goods are eaten up to their stock.** Harm is not a motive (P5), so with 411 g of wine per person available, all of it is drunk (43.6 g alcohol a day); sugar reaches 214 g a day. If people should hold back, a per-good ceiling $u_g$ for wine, beer and sugar is the one-parameter way (values to source).
2. **The harm coefficients** that turn (14) into a health burden, and the data for tobacco.
3. **Prices:** how the shadow values (18) become gold prices in the goods economy.
