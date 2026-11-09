function CarteProduit({ produit, onAjouter }) {
    return (
        <div className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition duration-300 border border-gray-100">
            <div className="h-48 bg-gray-100 flex items-center justify-center text-gray-400">
                {produit.image ? (
                    <img src={produit.image} alt={produit.nom} className="h-full w-full object-cover" />
                ) : (
                    <span>[Image du produit]</span>
                )}
            </div>
            
            <div className="p-6">
                <div className="flex justify-between items-start mb-2">
                    <h3 className="text-xl font-bold text-gray-900">{produit.nom}</h3>
                    <span className="text-xs font-semibold bg-blue-100 text-blue-800 px-2 py-1 rounded">
                        {produit.marque}
                    </span>
                </div>
                
                {/* Affichage des specs techniques */}
                <div className="text-sm text-gray-600 mb-4 space-y-1 mt-2">
                    {produit.processeur && <p>⚙️ {produit.processeur}</p>}
                    {produit.carte_graphique && <p>🎮 {produit.carte_graphique}</p>}
                    {produit.ram && <p>💾 {produit.ram}</p>}
                    {produit.stockage && <p>💽 {produit.stockage}</p>}
                </div>
                
                <div className="flex justify-between items-center mt-4 border-t pt-4">
                    <span className="text-2xl font-bold text-black">{produit.prix} AED</span>
                    <button 
                        onClick={() => onAjouter(produit)}
                        className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 transition active:scale-95 font-medium"
                    >
                        Ajouter
                    </button>
                </div>
            </div>
        </div>
    );
}

export default CarteProduit;