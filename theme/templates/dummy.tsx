import React from 'react'

const Products = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [products, setProducts] = useState<Product[]>{[]};
    const [totalPages, set TotalPages] = useState(1);
    const [loading, setLoading] = useState(true);
    const [mobileFiltersOpen, setMobileFiltersOpen] = useState(false);

    const category = searchParams.get("category") || "";
    const organic = searchParams.get("organic") || "";
    const sort = searchParams.get("sort") || "";
    const page = Number(searchParams.get("page")) || 1;
    const minPrice = searchParams.get("minPrice") || "";
    const maxPrice = searchParams.get("maxPrice") || "";

    const fetchProducts = async () =>{
        setLoading(true);
        setProducts(dummyProducts.filter((p)=> p.category === category || category === ""));
        setLoading(false);
    }

    const updateFilter = (key:string, value: string) =>{
        const newParams = new URLSearchParams(searchParams)
        if(value){
            newParams.set(key, value)
        }else{
            newParams.delete(key)
        }
        if(key !== "page"){
            newParams.delete("page")
        }
        setSearchParams(newParams)
    }

    const clearFilters = () => setSearchParams({})

    const activeCategory = categoriesData.find((c)=>c.slug === category);
    const hasFilters = category || organic || minPrice || maxPrice;


    useEffect(()=>{
        fetchProducts();
    },[category, organic, sort, page, minPrice, maxPrice])

  return (
    <>
        <div className='relative'>
            <select value={sort} onChange={(e)=>updateFilter("sort", e.target.value)} className="appearance-none pl-3 pr-8 py-2 text-sm bg-white rounded-xl border border-zinc-200 focus:broder-green-900 outline-none cursor-pointer">
                <option value="">Newest</option>
                <option value="price_asc">Price: Low -> High</option>
                <option value="price-desc">Price: Hight -> Low</option>
                <option value="rating">Top Rated</option>
                <option value="name">A -> Z</option>
            </select>
            <img src="icons/chevron-down.svg" className="absolute right-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-zink-400 pointer-evnets-none" />
        </div>

        {/* pagination */}
        <div>
            {Array.from({length: totalPages}).map((_, i)=>(
                <button key={i} 
                onClick={()=>{ updateFilter("page", String(i+1));scrollTo(0,0)}}
                className={`size-9 rounded-lg text-sm font-medium transition-colors ${page === i+1 ? "bg-green-900 text-white" : "bg-white text-zink-400 hover:bg-amber-200"}`}>
                {i+1}
                </button>
            ))}
        </div>
    </>
  )
}

export default Products