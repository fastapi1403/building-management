@echo off
setlocal enabledelayedexpansion

:: Set metadata
set CURRENT_DATE=2025-01-05
set CURRENT_TIME=10:30:24
set AUTHOR=hnejadi

echo Creating Units Template files...

:: Create directory structure
mkdir src\templates\units 2>nul
mkdir src\templates\units\components 2>nul
cd src\templates\units

:: Create index.html
echo {% extends "base/base.html" %}> index.html
echo {% block title %}Units Management{% endblock %}>> index.html
echo.>> index.html
echo {% block content %}>> index.html
echo ^<div class="units-container"^>>> index.html
echo     ^<h1^>Units Management^</h1^>>> index.html
echo     {% include "units/components/unit_filters.html" %}>> index.html
echo     ^<div class="units-content"^>>> index.html
echo         {% include "units/components/unit_list.html" %}>> index.html
echo     ^</div^>>> index.html
echo ^</div^>>> index.html
echo {% endblock %}>> index.html

:: Create details.html
echo {% extends "base/base.html" %}> details.html
echo {% block title %}Unit Details - {{ unit.number }}{% endblock %}>> details.html
echo.>> details.html
echo {% block content %}>> details.html
echo ^<div class="unit-details-container"^>>> details.html
echo     ^<div class="unit-header"^>>> details.html
echo         ^<h1^>Unit {{ unit.number }}^</h1^>>> details.html
echo         ^<div class="unit-actions"^>>> details.html
echo             ^<button class="btn btn-primary" onclick="editUnit({{ unit.id }})"^>Edit Unit^</button^>>> details.html
echo             ^<button class="btn btn-danger" onclick="showDeleteModal({{ unit.id }})"^>Delete Unit^</button^>>> details.html
echo         ^</div^>>> details.html
echo     ^</div^>>> details.html
echo     ^<div class="unit-info-grid"^>>> details.html
echo         ^<div class="info-card"^>>> details.html
echo             ^<h3^>Basic Information^</h3^>>> details.html
echo             ^<p^>^<strong^>Building:^</strong^> {{ unit.building.name }}^</p^>>> details.html
echo             ^<p^>^<strong^>Floor:^</strong^> {{ unit.floor }}^</p^>>> details.html
echo             ^<p^>^<strong^>Area:^</strong^> {{ unit.area }} m²^</p^>>> details.html
echo             ^<p^>^<strong^>Status:^</strong^> ^<span class="status-badge {{ unit.status | lower }}"^>{{ unit.status }}^</span^>^</p^>>> details.html
echo         ^</div^>>> details.html
echo         ^<div class="info-card"^>>> details.html
echo             ^<h3^>Current Tenant^</h3^>>> details.html
echo             {% if unit.tenant %}>> details.html
echo             ^<p^>^<strong^>Name:^</strong^> {{ unit.tenant.name }}^</p^>>> details.html
echo             ^<p^>^<strong^>Contact:^</strong^> {{ unit.tenant.contact }}^</p^>>> details.html
echo             ^<p^>^<strong^>Lease Period:^</strong^> {{ unit.tenant.lease_start | date }} - {{ unit.tenant.lease_end | date }}^</p^>>> details.html
echo             {% else %}>> details.html
echo             ^<p^>No current tenant^</p^>>> details.html
echo             {% endif %}>> details.html
echo         ^</div^>>> details.html
echo     ^</div^>>> details.html
echo     {% include "units/components/unit_history.html" %}>> details.html
echo     {% include "units/components/unit_maintenance.html" %}>> details.html
echo ^</div^>>> details.html
echo {% endblock %}>> details.html

cd components

:: Create unit_list.html
echo ^<div class="units-grid"^>> unit_list.html
echo     {% for unit in units %}>> unit_list.html
echo     ^<div class="unit-card {{ unit.status | lower }}"^>>> unit_list.html
echo         ^<div class="unit-header"^>>> unit_list.html
echo             ^<h3^>Unit {{ unit.number }}^</h3^>>> unit_list.html
echo             ^<span class="status-badge"^>{{ unit.status }}^</span^>>> unit_list.html
echo         ^</div^>>> unit_list.html
echo         ^<div class="unit-info"^>>> unit_list.html
echo             ^<p^>^<i class="fas fa-building"^>^</i^> {{ unit.building.name }}^</p^>>> unit_list.html
echo             ^<p^>^<i class="fas fa-ruler-combined"^>^</i^> {{ unit.area }} m²^</p^>>> unit_list.html
echo             ^<p^>^<i class="fas fa-money-bill-wave"^>^</i^> {{ unit.rent | currency }}/month^</p^>>> unit_list.html
echo         ^</div^>>> unit_list.html
echo         ^<div class="unit-actions"^>>> unit_list.html
echo             ^<a href="{{ url_for('units.details', id=unit.id) }}" class="btn btn-info"^>View^</a^>>> unit_list.html
echo             ^<button class="btn btn-primary" onclick="editUnit({{ unit.id }})"^>Edit^</button^>>> unit_list.html
echo         ^</div^>>> unit_list.html
echo     ^</div^>>> unit_list.html
echo     {% endfor %}>> unit_list.html
echo ^</div^>>> unit_list.html

:: Create unit_history.html
echo ^<div class="unit-history"^>> unit_history.html
echo     ^<h3^>Unit History^</h3^>>> unit_history.html
echo     ^<div class="history-timeline"^>>> unit_history.html
echo         {% for event in unit_history %}>> unit_history.html
echo         ^<div class="timeline-item"^>>> unit_history.html
echo             ^<div class="timeline-date"^>>> unit_history.html
echo                 {{ event.date | date }}>> unit_history.html
echo             ^</div^>>> unit_history.html
echo             ^<div class="timeline-content"^>>> unit_history.html
echo                 ^<h4^>{{ event.type }}^</h4^>>> unit_history.html
echo                 ^<p^>{{ event.description }}^</p^>>> unit_history.html
echo                 {% if event.amount %}>> unit_history.html
echo                 ^<p class="amount"^>{{ event.amount | currency }}^</p^>>> unit_history.html
echo                 {% endif %}>> unit_history.html
echo             ^</div^>>> unit_history.html
echo         ^</div^>>> unit_history.html
echo         {% endfor %}>> unit_history.html
echo     ^</div^>>> unit_history.html
echo ^</div^>>> unit_history.html

:: Create unit_maintenance.html
echo ^<div class="unit-maintenance"^>> unit_maintenance.html
echo     ^<h3^>Maintenance Records^</h3^>>> unit_maintenance.html
echo     ^<div class="maintenance-list"^>>> unit_maintenance.html
echo         ^<table class="table"^>>> unit_maintenance.html
echo             ^<thead^>>> unit_maintenance.html
echo                 ^<tr^>>> unit_maintenance.html
echo                     ^<th^>Date^</th^>>> unit_maintenance.html
echo                     ^<th^>Type^</th^>>> unit_maintenance.html
echo                     ^<th^>Description^</th^>>> unit_maintenance.html
echo                     ^<th^>Cost^</th^>>> unit_maintenance.html
echo                     ^<th^>Status^</th^>>> unit_maintenance.html
echo                 ^</tr^>>> unit_maintenance.html
echo             ^</thead^>>> unit_maintenance.html
echo             ^<tbody^>>> unit_maintenance.html
echo                 {% for record in maintenance_records %}>> unit_maintenance.html
echo                 ^<tr^>>> unit_maintenance.html
echo                     ^<td^>{{ record.date | date }}^</td^>>> unit_maintenance.html
echo                     ^<td^>{{ record.type }}^</td^>>> unit_maintenance.html
echo                     ^<td^>{{ record.description }}^</td^>>> unit_maintenance.html
echo                     ^<td^>{{ record.cost | currency }}^</td^>>> unit_maintenance.html
echo                     ^<td^>^<span class="status-badge {{ record.status | lower }}"^>{{ record.status }}^</span^>^</td^>>> unit_maintenance.html
echo                 ^</tr^>>> unit_maintenance.html
echo                 {% endfor %}>> unit_maintenance.html
echo             ^</tbody^>>> unit_maintenance.html
echo         ^</table^>>> unit_maintenance.html
echo     ^</div^>>> unit_maintenance.html
echo ^</div^>>> unit_maintenance.html

:: Create unit_filters.html
echo ^<div class="unit-filters"^>> unit_filters.html
echo     ^<form id="unit-filter-form" class="filter-form"^>>> unit_filters.html
echo         ^<div class="filter-group"^>>> unit_filters.html
echo             ^<label for="building-filter"^>Building:^</label^>>> unit_filters.html
echo             ^<select id="building-filter" name="building"^>>> unit_filters.html
echo                 ^<option value=""^>All Buildings^</option^>>> unit_filters.html
echo                 {% for building in buildings %}>> unit_filters.html
echo                 ^<option value="{{ building.id }}"^>{{ building.name }}^</option^>>> unit_filters.html
echo                 {% endfor %}>> unit_filters.html
echo             ^</select^>>> unit_filters.html
echo         ^</div^>>> unit_filters.html
echo         ^<div class="filter-group"^>>> unit_filters.html
echo             ^<label for="status-filter"^>Status:^</label^>>> unit_filters.html
echo             ^<select id="status-filter" name="status"^>>> unit_filters.html
echo                 ^<option value=""^>All Statuses^</option^>>> unit_filters.html
echo                 ^<option value="occupied"^>Occupied^</option^>>> unit_filters.html
echo                 ^<option value="vacant"^>Vacant^</option^>>> unit_filters.html
echo                 ^<option value="maintenance"^>Under Maintenance^</option^>>> unit_filters.html
echo             ^</select^>>> unit_filters.html
echo         ^</div^>>> unit_filters.html
echo         ^<div class="filter-group"^>>> unit_filters.html
echo             ^<label for="area-filter"^>Area (m²):^</label^>>> unit_filters.html
echo             ^<input type="number" id="area-min" name="area_min" placeholder="Min"^>>> unit_filters.html
echo             ^<input type="number" id="area-max" name="area_max" placeholder="Max"^>>> unit_filters.html
echo         ^</div^>>> unit_filters.html
echo         ^<button type="submit" class="btn btn-primary"^>Apply Filters^</button^>>> unit_filters.html
echo         ^<button type="reset" class="btn btn-secondary"^>Reset^</button^>>> unit_filters.html
echo     ^</form^>>> unit_filters.html
echo ^</div^>>> unit_filters.html

echo.
echo Units template files created successfully!
echo.
echo Created files:
echo - index.html
echo - details.html
echo Components:
echo - unit_list.html
echo - unit_history.html
echo - unit_maintenance.html
echo - unit_filters.html
echo.
pause