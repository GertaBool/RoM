# The food model, worked example (specification version 3, M98)

The equation numbers and symbols are those of `food_model_spec.md`. All values are computed by `plan/tools/food_model.py` and `plan/tools/food_model_trace.py` from the data files, and are rounded for display.

**City E (rich city):**
- $N=100{,}000$;
- $\mathbf w=(w_{\mathrm{vig}},w_{\mathrm{act}},w_{\mathrm{sed}})=(0.2,\,0.4,\,0.4)$;
- stocks $S_g$ in tonnes: Cow 20,000; Dairy 150,000; Potato 60,000; Wheat 40,000; Apple 20,000; Sugar 8,000; Wine 15,000; Tea 400; Salt 500.

## M1. Availability, equation (1)

$$
a_g=\frac{S_g\cdot10^6}{365\cdot100{,}000}
$$

| $g$ | Cow | Dairy | Potato | Wheat | Apple | Sugar | Wine | Tea | Salt |
|---|---|---|---|---|---|---|---|---|---|
| $a_g$ [g/(p·d)] | 547.9 | 4,109.6 | 1,643.8 | 1,095.9 | 547.9 | 219.2 | 411.0 | 11.0 | 13.7 |

## M2. Need and bounds, equations (2)-(8)

$$
\begin{aligned}
(2)\quad & \text{tea: } \ell\chi/1000=43\cdot200/1000=8.6\ \text{mg/g};\quad q_{\mathrm{tea}}=\min(11.0,\;600/8.6)=11.0\ \text{g};\quad \text{caffeine}=94.2\ \text{mg};\quad c=94.2/600=0.157\\
(3)\quad & \Lambda^{\mathrm w}=0.2\cdot2.25+0.4\cdot1.76+0.4\cdot1.53=1.766\\
(4)\quad & E^{\mathrm{need}}=1536\cdot1.766+150\cdot0.157=2{,}735\ \text{kcal}\\
(5)\quad & E^{\max}=1536\cdot2.40+150\cdot0.157=3{,}709\ \text{kcal}\\
(6)\quad & F^{\mathrm{fed}}=1.36\cdot2{,}735=3{,}720;\qquad F^{\max}=1.36\cdot3{,}709=5{,}044\\
(7)\quad & P^{\max}=0.35\cdot3{,}709/4=324.5\ \text{g}\\
(8)\quad & q_{\mathrm{salt}}=\min(13.7,\,10)=10\ \text{g}
\end{aligned}
$$

## M3. Indicators per good, equations (9)-(16)

**Inputs from the data:**

| $g$ | $\varepsilon_g$ | $\pi_g$ | $\varphi_g$ | $\eta_g$ | $\delta_g$ | Holt $H_g$ |
|---|---|---|---|---|---|---|
| Cow (composite, 28) | 150 | 18.5 | 7.9 | 1.0 | 1.12 | 176 |
| Dairy | 61 | 3.3 | 3.3 | 1.0 | 1.14 | – (formula: 155) |
| Potato | 67 | 1.6 | 0.1 | 1.0 | 0.44 | 323 |
| Wheat | 334 | 12.2 | 2.3 | 0.8 | 0.44 | 157 (wholemeal bread) |
| Apple | 48 | 0.1 | 0.3 | 1.0 | 0.44 | 197 |
| Sugar | 373 | 0 | 0 | 1.0 | 0.44 | – (formula: 100) |
| Wine | 68 | 0 | 0 | 1.0 | 0.44 | – (formula: 140) |

**Results of (9)-(16):**

| $g$ | $e_g$ (9) | $p_g$ (10) | $\sigma_g$ (11) | $s_g$ (12) | $\nu_g$ (13) | $\beta_g$ (14) | $K^{(1)}_g$ (15) | $K^{(2)}_g$ (15) | $\bar q_g$ (16) |
|---|---|---|---|---|---|---|---|---|---|
| Cow | 1.500 | 0.493 | 1.76 | 1.760 | 0.710 | −0.139 | 2.470 | −0.139 | 548 |
| Dairy | 0.610 | 0.216 | 0.78 | 1.270 | 0.795 | 0.858 | 2.065 | 0.858 | 3,000 |
| Potato | 0.670 | 0.096 | 3.23 | 0.961 | 0.659 | 0.365 | 1.620 | 0.365 | 1,644 |
| Wheat | 2.672 | 0.146 | 1.57 | 1.000 | 0.551 | 0.133 | 1.551 | 0.133 | 1,096 |
| Apple | 0.480 | 0.008 | 1.97 | 0.893 | 0.462 | 1.491 | 1.355 | 1.491 | 548 |
| Sugar | 3.730 | 0.000 | 1.00 | 0.886 | 0.173 | 1.071 | 1.059 | 1.071 | 219 |
| Wine | 0.680 | 0.000 | 0.70 | 0.886 | 0.292 | 1.467 | 1.178 | 1.467 | 411 |

Units: $e_g$ in kcal/g; $\bar q_g$ in g/(p·d); the rest are dimensionless.

**One row in full: Cow.**

$$
\begin{aligned}
(9)\quad & e=150\cdot1.0/100=1.500;\qquad \hat\varphi=7.9/100=0.079\\
(10)\quad & p=4\cdot18.5/150=0.493;\quad f=9\cdot7.9/150=0.474;\quad k=1-0.474-0.493=0.033;\quad z=l=0\\
(11)\quad & \sigma=176/100=1.76\\
(12)\quad & s=\frac{1+2.0\cdot0.493\cdot1}{1+2.0\cdot0.146\cdot0.44}=\frac{1.986}{1.128}=1.760\\
(13)\quad & \nu=\tfrac{1}{13}\bigl(\underbrace{1}_{\text{prot}}+\underbrace{0}_{\text{C}}+\underbrace{1}_{\text{A}}+\underbrace{0.97}_{\text{B1}}+\underbrace{1}_{\text{B3}}+\underbrace{0.56}_{\text{fol}}+\underbrace{1}_{\text{B12}}+\underbrace{1}_{\text{Fe}}+\underbrace{1}_{\text{Zn}}+\underbrace{0.10}_{\text{Ca}}+\underbrace{0}_{\text{I}}+\underbrace{0.70}_{\text{K}}+\underbrace{0.90}_{\text{Na}}\bigr)=\tfrac{9.226}{13}=0.710\\
(14)\quad & \beta=1\cdot0+2\cdot0.474\cdot0.033+1\cdot0+1\cdot\min(1,0.201/3)-0.5\cdot0.474=0.031+0.067-0.237=-0.139\\
(15)\quad & K^{(1)}=1.760+0.710=2.470;\qquad K^{(2)}=-0.139\\
(16)\quad & \bar q=\min(547.9,\;250/0.079,\;\cdot)=\min(547.9,\,3165)=547.9
\end{aligned}
$$

## M4. Allocation, Algorithm 1 with (17)-(18)

| Pass | Key | Stops at | Ends with |
|---|---|---|---|
| 1 | $K^{(1)}$ (nutrition) | $F\ge F^{\mathrm{fed}}=3{,}720$ | $E=2{,}120$ kcal, $F=3{,}735$ |
| 2 | $K^{(2)}$ (well-being; only $K^{(2)}>0$, so Cow is out) | $F\ge F^{\max}=5{,}044$ | $E=3{,}300$ kcal, $F=5{,}062$ |

Result:

| $g$ | $q_g$ [g] | $e_gq_g$ [kcal] | $\sigma_ge_gq_g$ [fullness] | taken in pass |
|---|---|---|---|---|
| Cow | 333 | 500 | 880 | 1 |
| Dairy | 1,934 | 1,180 | 920 | 1, 2 |
| Potato | 851 | 570 | 1,841 | 1, 2 |
| Wheat | 135 | 360 | 565 | 1 |
| Apple | 542 | 260 | 512 | 1, 2 (stock) |
| Sugar | 43 | 160 | 160 | 1, 2 |
| Wine | 397 | 270 | 189 | 1, 2 (stock) |
| **Σ** | | **3,300** | **5,062** | |

A good can appear in both passes because (17) declines with $q_g$. Pass 2 continues the good from where pass 1 left it.

Check of property (P1), equation (29): $\tilde\sigma=5{,}062/3{,}300=1.534$, so $E=F/\tilde\sigma=3{,}300$ kcal. The stop overshoots $F^{\max}$ by 18, within one step (P3).

## M5. Outcomes, equations (19)-(27)

$$
\begin{aligned}
(19)\quad & \textit{fed}=5{,}062/3{,}720=1.36;\qquad x=3{,}300/2{,}735=1.21\\
(21)\quad & a^{\mathrm{Fe}}=0.10+0.08\cdot(\text{animal protein}/P)=0.166;\qquad P=152.8\ \text{g}\ (18.5\,\%\ \text{of energy})\\
(23)\quad & W^{\mathrm{food}}=1{,}325\ \text{ml};\qquad W^{\mathrm{drink}}=\underbrace{1934\cdot1.5}_{\text{milk}}+\underbrace{397}_{\text{wine}}+\underbrace{11.0\cdot43}_{\text{tea}}=3{,}770\ \text{ml}\\
(24)\quad & W^{\mathrm{plain}}=\max(0,\;2{,}250-1{,}325-3{,}770)=0\\
(25)\quad & \Lambda^{\mathrm{act}}=\min(2.40,\max(1.40,\;3{,}300/1{,}536))=2.149\\
(26)\quad & \textit{work}=\min(1.20,\;(2.149-1.40)/(1.766-1.40))=\min(1.20,\,2.05)=1.20
\end{aligned}
$$

**Coverage, (20) and (22):**

| $i$ | C | A | B1 | B3 | folate | B12 | Fe | Zn | Ca | I | K | Na |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $c_i$ | 1.82 | 2.46 | 3.37 | 2.42 | 1.18 | 5.82 | 2.76 | 2.73 | 3.18 | 2.12 | 2.36 | 8.30 |

**Stocks, (27), in tonnes:**

| $g$ | Cow | Dairy | Potato | Wheat | Apple | Sugar | Wine | Tea | Salt |
|---|---|---|---|---|---|---|---|---|---|
| $L_g$ | 7,833 | 79,393 | 28,948 | 35,082 | 229 | 6,434 | 507 | 0 | 135 |
| $D_g$ | 7,833 | 79,393 | 14,474 | 1,754 | 229 | 643 | 76 | 0 | 14 |

Fresh goods ($\bar\delta=1$) spoil whole; grain, sugar and wine keep. Milk converted to cheese before eating (recipes) is not in this example.
