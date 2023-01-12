--Cleaning Data

select *
from PortfolioProject.dbo.NashvilleHousing



--Standardize sale date
select SaleDateConverted
from PortfolioProject.dbo.NashvilleHousing

alter table NashvilleHousing
add SaleDateConverted Date;

update NashvilleHousing
set SaleDateConverted = CONVERT(Date, SaleDate)



--Populate property address
select *
from PortfolioProject.dbo.NashvilleHousing




select a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress,ISNULL(a.PropertyAddress, b.PropertyAddress)
from PortfolioProject.dbo.NashvilleHousing a
join PortfolioProject.dbo.NashvilleHousing b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null

update a
set PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
from PortfolioProject.dbo.NashvilleHousing a
join PortfolioProject.dbo.NashvilleHousing b
	on a.ParcelID = b.ParcelID
	and a.[UniqueID ] <> b.[UniqueID ]
where a.PropertyAddress is null




--breaking Address into different columns (Address, city, state)
select PropertyAddress
from PortfolioProject.dbo.NashvilleHousing


select
SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress) -1) as Address
, SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) +1, len(PropertyAddress)) as City
from PortfolioProject.dbo.NashvilleHousing

alter table NashvilleHousing
add PropertySplitAddress nvarchar(255);

update NashvilleHousing
set PropertySplitAddress = SUBSTRING(PropertyAddress, 1, CHARINDEX(',', PropertyAddress) -1)

alter table NashvilleHousing
add PropertySplitCity nvarchar(255);

update NashvilleHousing
set PropertySplitCity = SUBSTRING(PropertyAddress, CHARINDEX(',', PropertyAddress) +1, len(PropertyAddress))

select *
from PortfolioProject.dbo.NashvilleHousing



--Parsing Owner Address
select OwnerAddress
from PortfolioProject.dbo.NashvilleHousing

select PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3) as OwnerAddressParsed,
PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2) as OwnerCityParsed,
PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1) as OwnerStateParsed
from PortfolioProject.dbo.NashvilleHousing


alter table PortfolioProject.dbo.NashvilleHousing
add OwnerAddressParsed nvarchar(255);

update PortfolioProject.dbo.NashvilleHousing
set OwnerAddressParsed = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 3)


alter table PortfolioProject.dbo.NashvilleHousing
add OwnerCityParsed nvarchar(255);

update PortfolioProject.dbo.NashvilleHousing
set OwnerCityParsed = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 2)


alter table PortfolioProject.dbo.NashvilleHousing
add OwnerStateParsed nvarchar(255);

update PortfolioProject.dbo.NashvilleHousing
set OwnerStateParsed = PARSENAME(REPLACE(OwnerAddress, ',', '.'), 1)



select *
from PortfolioProject.dbo.NashvilleHousing



--change y and n to yes and no
select distinct(SoldAsVacant), count(SoldAsVacant)
from PortfolioProject.dbo.NashvilleHousing
group by SoldAsVacant
order by 2


select SoldAsVacant
, case when SoldAsVacant = 'Y' then 'Yes'
	   when SoldAsVacant = 'N' then 'No'
	   else SoldAsVacant
	   end
from PortfolioProject.dbo.NashvilleHousing

update PortfolioProject.dbo.NashvilleHousing
set SoldAsVacant = case when SoldAsVacant = 'Y' then 'Yes'
	   when SoldAsVacant = 'N' then 'No'
	   else SoldAsVacant
	   end
from PortfolioProject.dbo.NashvilleHousing



--Remove Duplicates
with RowNumCTE as (
select *,
	ROW_NUMBER() over (
	partition by ParcelID,
				 PropertyAddress,
				 SalePrice,
				 SaleDate,
				 LegalReference
				 order by
				  UniqueID
				  ) row_num
from PortfolioProject.dbo.NashvilleHousing
)

delete
from RowNumCTE
where row_num > 1



--Delete unused columns
alter table PortfolioProject.dbo.NashvilleHousing
drop column OwnerAddress, TaxDistrict, PropertyAddress;

alter table PortfolioProject.dbo.NashvilleHousing
drop column SaleDate;