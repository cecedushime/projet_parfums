function CarteParfum({ parfum, onAjouter }) {
    return (
        <div className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition duration-300">
            <div className="h-48 bg-gray-200 flex items-center justify-center text-gray-500">
                [Image du parfum]
            </div>
            
            <div className="p-6">
                <h3 className="text-xl font-bold mb-2 text-gray-900">{parfum.nom}</h3>
                <p className="text-gray-600 mb-4">{parfum.marque}</p>
                
                <div className="flex justify-between items-center mt-4">
                    <span className="text-2xl font-bold text-black">{parfum.prix} AED</span>
                    <button 
                        onClick={() => onAjouter(parfum)}
                        className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 transition active:scale-95"
                    >
                        Ajouter
                    </button>
                </div>
            </div>
        </div>
    );
}

export default CarteParfum;