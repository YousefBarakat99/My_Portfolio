select *
from PortfolioProject.dbo.CovidDeaths
order by 3,4

--select *
--from PortfolioProject.dbo.CovidVaccinations
--order by 3,4

--select dates we will be using

select location, date, total_cases, new_cases, total_deaths, population
from PortfolioProject.dbo.CovidDeaths
order by location, date


--total cases vs total deaths
--likelihood of dying from covid in your country
select location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 as Death_Percentage
from PortfolioProject.dbo.CovidDeaths
where location like '%egypt%'
order by location, date


--total cases vs population
--shows percentage of population with covid
select location, date, total_cases, population, (total_cases/population)*100 as Population_Percentage
from PortfolioProject.dbo.CovidDeaths
where location like '%egypt%'
order by location, date


--countries with highest infection rate vs population
select location, population, max(total_cases) as Infection_Count, (max(total_cases)/population)*100 as Population_Percentage
from PortfolioProject.dbo.CovidDeaths
--where location like '%egypt%'
group by location, population
order by Population_Percentage desc


--infection count and percentage along the days
select location, population, date, max(total_cases) as Infection_Count, (max(total_cases)/population)*100 as Population_Percentage
from PortfolioProject.dbo.CovidDeaths
--where location like '%egypt%'
group by location, population, date
order by Population_Percentage desc


--showing countries with highest death count
select location, max(cast(total_deaths as int)) as TotalDeathCount
from PortfolioProject.dbo.CovidDeaths
where continent is not null
--where location like '%egypt%'
group by location
order by TotalDeathCount desc


--showing continets with highest death count (correct way)
select location, max(cast(total_deaths as int)) as TotalDeathCount
from PortfolioProject.dbo.CovidDeaths
where continent is null and location not in ('World', 'European Union', 'International')
group by location
order by TotalDeathCount desc


--showing continets with highest death count
select continent, max(cast(total_deaths as int)) as TotalDeathCount
from PortfolioProject.dbo.CovidDeaths
where continent is not null
group by continent
order by TotalDeathCount desc


--total cases globally per day
select date, sum(new_cases) as TotalCases, sum(cast(new_deaths as int)) as TotalDeaths, (sum(cast(new_deaths as int))/sum(new_cases))*100 as DeathPercent
from PortfolioProject.dbo.CovidDeaths
where continent is not null
group by date
order by date

--total cases overall 
select sum(new_cases) as TotalCases, sum(cast(new_deaths as int)) as TotalDeaths, (sum(cast(new_deaths as int))/sum(new_cases))*100 as DeathPercent
from PortfolioProject.dbo.CovidDeaths
where continent is not null
--group by date
--order by date



select *
from PortfolioProject.dbo.CovidVaccinations


--joining 2 tables together
select *
from PortfolioProject.dbo.CovidDeaths death
join PortfolioProject.dbo.CovidVaccinations vax
	on death.location = vax.location
	and death.date = vax.date


--total population vs vaccinations
select death.continent, death.location, death.date, death.population, vax.new_vaccinations, 
sum(convert(int, vax.new_vaccinations)) over (partition by death.location order by death.location, death.date) as TotalVaccinations
--(TotalVaccinations/death.population)*100 as VaccinatedPercentage
from PortfolioProject.dbo.CovidDeaths death
join PortfolioProject.dbo.CovidVaccinations vax
	on death.location = vax.location
	and death.date = vax.date
where death.continent is not null and death.location like '%states%'
order by 2, 3


--using CTE
with PopvsVax (continent, location, date, population, NewVaccinations, RollingVaccinations)
as
(
select death.continent, death.location, death.date, death.population, vax.new_vaccinations, 
sum(convert(int, vax.new_vaccinations)) over (partition by death.location order by death.location, death.date) as TotalVaccinations
from PortfolioProject.dbo.CovidDeaths death
join PortfolioProject.dbo.CovidVaccinations vax
	on death.location = vax.location
	and death.date = vax.date
where death.continent is not null --and death.location like '%states%'
)
select *, (RollingVaccinations/population)*100 as PercentageVaccinated
from PopvsVax



--temp table
drop table if exists #PercentPopulationVaccinated
create table  #PercentPopulationVaccinated
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_Vaccinations numeric,
RollingVaccinations numeric
)
insert into #PercentPopulationVaccinated
select death.continent, death.location, death.date, death.population, vax.new_vaccinations, 
sum(convert(int, vax.new_vaccinations)) over (partition by death.location order by death.location, death.date) as TotalVaccinations
from PortfolioProject.dbo.CovidDeaths death
join PortfolioProject.dbo.CovidVaccinations vax
	on death.location = vax.location
	and death.date = vax.date
where death.continent is not null --and death.location like '%states%'

select *, (RollingVaccinations/population)*100 as PercentageVaccinated
from #PercentPopulationVaccinated
order by 2,3


--creating view to store data to visualize
create view PercentPopulationVaccinated as
select death.continent, death.location, death.date, death.population, vax.new_vaccinations, 
sum(convert(int, vax.new_vaccinations)) over (partition by death.location order by death.location, death.date) as TotalVaccinations
from PortfolioProject.dbo.CovidDeaths death
join PortfolioProject.dbo.CovidVaccinations vax
	on death.location = vax.location
	and death.date = vax.date
where death.continent is not null