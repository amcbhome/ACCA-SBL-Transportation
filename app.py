\documentclass[10pt,a4paper,sans]{moderncv}

% --- MODERNCV CONFIGURATION ---
\moderncvstyle{banking}
\moderncvcolor{blue} 

% Expanded printable area to fit cleanly on one page
\usepackage[top=1.2cm, bottom=1.2cm, left=1.4cm, right=1.4cm]{geometry}
\usepackage{enumitem}
\usepackage{lmodern}

% Reduce vertical spacing around titles and sections
\nopagenumbers{}
\setlength{\subseconflictspace}{0pt}
\setlength{\hintscolumnwidth}{2.5cm}

% --- PERSONAL INFORMATION ---
\name{Alastair}{McBride}
\title{BAcc (Hons) -- Accounting \& Business Analytics}
\address{Ayrshire}{Scotland}{}
\email{email@example.com}
\homepage{github.com/amcbhome}

\begin{document}

\makecvtitle
\vspace{-22pt}

% --- EXECUTIVE SUMMARY ---
\section{Professional Summary}
\vspace{-2pt}
Accounting graduate (2:1 Honours) with fundamental ACCA exemptions (F1--F9) combining financial management expertise with quantitative business analytics. Proficient in prescriptive data modeling, linear programming, Python analytics, SQL, and inventory data collection. Proven track record of building operational optimization tools and auditing inventory environments, seeking to apply data modeling and financial acumen as a \textbf{Business Analyst} in the FMCG sector.

\vspace{-4pt}

% --- EDUCATION & PROFESSIONAL QUALIFICATIONS ---
\section{Education \& Professional Qualifications}
\cventry{2021 -- 2025}{Bachelor of Accountancy with Honours (BAcc Hons) --- 2:1}{University of the West of Scotland (UWS)}{Scotland}{}{%
\begin{itemize}[leftmargin=*, itemsep=0pt, topsep=1pt]
    \item \textbf{ACCA Exemptions:} Qualified for fundamental level exemptions from papers F1 through F9.
    \item \textbf{Core Modules:} Management Accounting, APM, SBL, Financial Management, Quantitative Business Analysis.
\end{itemize}}
\vspace{-3pt}
\cventry{2026 -- Present}{Business Administration Training}{Maximus}{Scotland}{}{}
\vspace{-3pt}
\cventry{Completed}{Personal Development Award (PDA) in Bookkeeping}{Achieved during HNC}{Scotland}{}{}

\vspace{-4pt}

% --- TECHNICAL & ANALYTICAL SKILLS ---
\section{Technical \& Analytical Skills}
\cvitem{Programming}{Python (\texttt{PuLP}, \texttt{pandas}, \texttt{NumPy}), SQL, Streamlit, Git / GitHub}
\cvitem{Analytics}{Prescriptive \& Predictive Analytics, Linear Programming, Sensitivity Analysis, Apache Superset}
\cvitem{Operations}{Purchases Ledger, Stock Auditing, Inventory Control, Accounting Governance, Process Optimization}

\vspace{-4pt}

% --- DATA ANALYTICS & PORTFOLIO PROJECTS ---
\section{Data Analytics \& Portfolio Projects}
\vspace{-2pt}
\textit{Independent technical portfolio demonstrating the transition of traditional accounting framework models (Excel Solver) into automated Python algorithms and interactive Business Intelligence (BI) applications.}

\vspace{2pt}

\cventry{2026}{Prescriptive Supply Chain Transportation Optimizer}{Python | PuLP | Streamlit | Git}{}{}{%
\textit{Project Repository: \href{https://github.com/amcbhome/delivery-LP}{github.com/amcbhome/delivery-LP}}
\begin{itemize}[leftmargin=*, itemsep=1pt, topsep=1pt]
    \item \textbf{Prescriptive Freight Optimization:} Modeled multi-depot FMCG distribution routes in Python using \texttt{PuLP}, modernizing legacy spreadsheet tools with scalable Simplex LP algorithms to minimize freight costs ($\text{\pounds}/\text{unit}/\text{mile}$).
    \item \textbf{Capacity \& Slack Analytics:} Programmed automated constraint evaluation to measure non-binding slack—identifying \textbf{150 units of unallocated storage space} at Store 2 to support promotional buffering and reduce holding costs.
    \item \textbf{Automated BI Dashboard:} Built an interactive Streamlit app serving as an automated BI tool featuring dynamic mileage rates, operational controls, and integer dispatch schedules.
    \item \textbf{Enterprise Code Architecture:} Maintained a structured, version-controlled repository on GitHub adhering to PEP 8 standards, engineered to interface with enterprise SQL/ERP data pipelines.
\end{itemize}}

\vspace{-4pt}

% --- PROFESSIONAL EXPERIENCE ---
\section{Professional Experience}
\cventry{Current}{Stock Counter (Data Collector)}{Retail Asset Solutions}{Casual Contract}{}{%
\begin{itemize}[leftmargin=*, itemsep=0pt, topsep=1pt]
    \item Conduct physical stock counts and operational data collection across commercial retail store environments.
    \item Execute systematic inventory audits to ensure high ledger accuracy and minimize stock variance.
\end{itemize}}
\vspace{-3pt}
\cventry{Jul 2025 -- Dec 2025}{General Operative}{Atlas FM}{Ayrshire}{}{%
\begin{itemize}[leftmargin=*, itemsep=0pt, topsep=1pt]
    \item Managed facility maintenance and operational workflows to ensure compliance with health and safety standards.
\end{itemize}}
\vspace{-3pt}
\cventry{1988 -- 1993}{Quality Control Technician}{Isola UK Ltd}{Cumbernauld}{}{%
\begin{itemize}[leftmargin=*, itemsep=0pt, topsep=1pt]
    \item Performed technical quality testing, process control verification, and statistical sampling for manufacturing outputs.
\end{itemize}}

\end{document}
