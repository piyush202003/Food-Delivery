import React from 'react'

const FilterPanel = ({categories, category, minPrice, maxPrice, updateFilter, clearFilters, hasFilters}:any) => {
    const categoriesWithAll = [{slug: "", name: "All Categories"}, ...categories]

  return (
    <div className="space-y-6">
        {/* categories */}
        <div>
            <h3>categories</h3>
            <div>{categoriesWithAll.map((cat:any)=>(
                
            ))}</div>
        </div>
    </div>
  )
}

export default FilterPanel