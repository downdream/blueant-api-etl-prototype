async function loadProjects() {
    try {
        const response = await fetch("/api/projects");

        if (!response.ok) {
            throw new Error("Failed to load projects");
        }

        const data = await response.json();

        showPortfolioInfo(data.portfolio, data.ki_portfolio_projects);
        fillProjectDropdown(data.projects);
    } catch (error) {
        console.error("Error loading projects:", error);

        const portfolioInfo = document.getElementById("portfolio-info");
        portfolioInfo.textContent = "Fehler beim Laden der Projektdaten.";
    }
}


function showPortfolioInfo(portfolio, projectCount) {
    const portfolioInfo = document.getElementById("portfolio-info");

    portfolioInfo.textContent = `Portfolio: ${portfolio.name} | Projekte: ${projectCount}`;
}


function fillProjectDropdown(projects) {
    const projectSelect = document.getElementById("project-select");

    projects.forEach((project) => {
        const option = document.createElement("option");

        option.value = project.id;
        option.textContent = `${project.number} - ${project.name}`;

        projectSelect.appendChild(option);
    });
}

async function loadProjectDashboard(projectId) {
    try {
        const response = await fetch(`/api/projects/${projectId}/dashboard`);

        if (!response.ok) {
            throw new Error("Failed to load project dashboard");
        }

        const data = await response.json();

        showProjectDetails(data.project);
        showKpis(data.project.kpis);
        showIndicators(data.project.indicators);
        showPlanning(data.planning);

    } catch (error) {
        console.error("Error loading project dashboard:", error);

        const projectDetails = document.getElementById("project-details");
        projectDetails.innerHTML = `
            <h2>Projekt Details</h2>
            <p>Fehler beim Laden der Projektdetails.</p>
        `;
    }
}


function showProjectDetails(project) {
    const projectDetails = document.getElementById("project-details");

    projectDetails.innerHTML = `
        <h2>Projekt Details</h2>
        <h3>${project.number} - ${project.name}</h3>
        <p><strong>Start:</strong> ${project.start}</p>
        <p><strong>Ende:</strong> ${project.end}</p>
        <p><strong>Planungstyp:</strong> ${project.planning_type}</p>
        <p><strong>Abrechnungstyp:</strong> ${project.billing_type}</p>

        <h4>Gegenstand</h4>
        <p>${project.subject || "Keine Angabe"}</p>

        <h4>Problem</h4>
        <p>${project.problem || "Keine Angabe"}</p>

        <h4>Ziel</h4>
        <p>${project.objective || "Keine Angabe"}</p>

        <h4>Statusbericht</h4>
        <p>${project.status_text || "Keine Angabe"}</p>
    `;
}

function showKpis(kpis) {
    const kpiCards = document.getElementById("kpi-cards");

    kpiCards.innerHTML = `
        <div>
            <strong>Projektbudget:</strong> ${formatCurrency(kpis.project_budget_eur)}
        </div>
        <div>
            <strong>Plankosten:</strong> ${formatCurrency(kpis.planned_costs_eur)}
        </div>
        <div>
            <strong>IST-Kosten:</strong> ${formatCurrency(kpis.actual_costs_eur)}
        </div>
        <div>
            <strong>Plan Aufwand bis heute:</strong> ${formatNumber(kpis.planned_effort_until_today_pt)} PT
        </div>
        <div>
            <strong>Plan Aufwand gesamt:</strong> ${formatNumber(kpis.planned_effort_total_pt)} PT
        </div>
        <div>
            <strong>Ist Aufwand:</strong> ${formatNumber(kpis.actual_effort_pt)} PT
        </div>
        <div>
            <strong>Plan Fertigstellung:</strong> ${formatPercent(kpis.planned_completion_percent)}
        </div>
        <div>
            <strong>Ist Fertigstellung:</strong> ${formatPercent(kpis.actual_completion_percent)}
        </div>
    `;
}

function showIndicators(indicators) {
    const indicatorCards = document.getElementById("indicator-cards");

    indicatorCards.innerHTML = `
        <div>
            <strong>Status Gesamt:</strong> ${formatLabel(indicators.status_total?.label)}
        </div>
        <div>
            <strong>Status Ergebnis:</strong> ${formatLabel(indicators.status_result?.label)}
        </div>
        <div>
            <strong>Status Zeit:</strong> ${formatLabel(indicators.status_time?.label)}
        </div>
        <div>
            <strong>Status Aufwand:</strong> ${formatLabel(indicators.status_effort?.label)}
        </div>
        <div>
            <strong>Fortschritt:</strong> ${formatPercent(indicators.progress_percent)}
        </div>
        <div>
            <strong>Klassifikation:</strong> ${formatLabel(indicators.classification?.label)}
        </div>
        <div>
            <strong>Strategiebeitrag:</strong> ${formatLabel(indicators.strategy_contribution?.label)}
        </div>
        <div>
            <strong>Vertraulichkeit:</strong> ${formatLabel(indicators.confidentiality?.label)}
        </div>
        <div>
            <strong>Erläuterung Status:</strong> ${formatLabel(indicators.status_explanation)}
        </div>
    `;
}

function formatCurrency(value) {
    if (value === null || value === undefined) {
        return "Keine Angabe";
    }

    return new Intl.NumberFormat("de-DE", {
        style: "currency",
        currency: "EUR",
    }).format(value);
}


function formatNumber(value) {
    if (value === null || value === undefined) {
        return "Keine Angabe";
    }

    return new Intl.NumberFormat("de-DE", {
        maximumFractionDigits: 2,
    }).format(value);
}

function formatDate(value) {
    if (!value) {
        return "Keine Angabe";
    }

    return new Intl.DateTimeFormat("de-DE").format(new Date(value));
}

function formatPercent(value) {
    if (value === null || value === undefined) {
        return "Keine Angabe";
    }

    return `${formatNumber(value)} %`;
}

function formatLabel(value) {
    if (value === null || value === undefined || value === "") {
        return "Keine Angabe";
    }

    return value;
}

function showPlanning(planning) {
    const planningContent = document.getElementById("planning-content");

    const tasks = planning.tasks || [];
    const milestones = planning.milestones || [];

    planningContent.innerHTML = `
        <h3>Übersicht</h3>
        <p>
            <strong>Planungseinträge:</strong> ${planning.total_entries} |
            <strong>Tasks:</strong> ${planning.total_tasks} |
            <strong>Meilensteine:</strong> ${planning.total_milestones}
        </p>

        <h3>Meilensteine</h3>
        ${createMilestoneTable(milestones)}

        <h3>Tasks / Arbeitspakete</h3>
        ${createTaskTable(tasks)}
    `;
}

function createMilestoneTable(milestones) {
    if (!milestones.length) {
        return "<p>Keine Meilensteine vorhanden.</p>";
    }

    const rows = milestones.map((milestone) => `
        <tr>
            <td>${formatLabel(milestone.number)}</td>
            <td>${formatLabel(milestone.name)}</td>
            <td>${formatDate(milestone.start)}</td>
            <td>${formatLabel(milestone.progress_actual)}</td>
        </tr>
    `).join("");

    return `
        <table>
            <thead>
                <tr>
                    <th>Nr.</th>
                    <th>Name</th>
                    <th>Datum</th>
                    <th>Fortschritt</th>
                </tr>
            </thead>
            <tbody>
                ${rows}
            </tbody>
        </table>
    `;
}


function createTaskTable(tasks) {
    if (!tasks.length) {
        return "<p>Keine Tasks vorhanden.</p>";
    }

    const rows = tasks.map((task) => `
        <tr>
            <td>${formatLabel(task.number)}</td>
            <td>${formatLabel(task.name)}</td>
            <td>${formatDate(task.start)}</td>
            <td>${formatDate(task.end)}</td>
            <td>${formatNumber(task.work_planned_days)} PT</td>
            <td>${formatNumber(task.work_actual_days)} PT</td>
        </tr>
    `).join("");

    return `
        <table>
            <thead>
                <tr>
                    <th>Nr.</th>
                    <th>Name</th>
                    <th>Start</th>
                    <th>Ende</th>
                    <th>Plan</th>
                    <th>Ist</th>
                </tr>
            </thead>
            <tbody>
                ${rows}
            </tbody>
        </table>
    `;
}

document.addEventListener("DOMContentLoaded", () => {
    loadProjects();

    const projectSelect = document.getElementById("project-select");

    projectSelect.addEventListener("change", (event) => {
        const projectId = event.target.value;

        if (projectId) {
            loadProjectDashboard(projectId);
        }
    });
});