function PanneauPanier({ panier, onFermer, onSupprimer, onCommander, isCommandeEnCours }) {
    const total = panier.reduce((acc, item) => acc + (parseFloat(item.prix) * item.quantite), 0);

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-end z-50">
            <div className="bg-white w-full max-w-md h-full shadow-2xl flex flex-col">
                <div className="flex justify-between items-center p-6 border-b">
                    <h2 className="text-2xl font-bold text-gray-800">Votre Panier</h2>
                    <button onClick={onFermer} className="text-gray-500 hover:text-red-500 text-3xl font-bold">
                        &times;
                    </button>
                </div>

                <div className="flex-1 overflow-y-auto p-6">
                    {panier.length === 0 ? (
                        <p className="text-gray-500 text-center mt-10">Votre panier est vide.</p>
                    ) : (
                        <ul className="space-y-4">
                            {panier.map(item => (
                                <li key={item.id} className="flex justify-between items-center border-b pb-4">
                                    <div>
                                        <h4 className="font-bold text-gray-800">{item.nom}</h4>
                                        <p className="text-sm text-gray-500">Quantité : {item.quantite}</p>
                                        <p className="text-gray-800 font-semibold">{item.prix} AED</p>
                                    </div>
                                    <button 
                                        onClick={() => onSupprimer(item.id)}
                                        className="text-red-500 hover:text-red-700 text-sm font-semibold"
                                    >
                                        Supprimer
                                    </button>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>

                <div className="p-6 border-t bg-gray-50">
                    <div className="flex justify-between items-center mb-4">
                        <span className="text-lg font-bold text-gray-800">Total :</span>
                        <span className="text-2xl font-bold text-black">{total.toFixed(2)} AED</span>
                    </div>
                    
                    <button 
                        onClick={onCommander}
                        disabled={panier.length === 0 || isCommandeEnCours}
                        className="w-full bg-black text-white py-3 rounded font-bold hover:bg-gray-800 transition disabled:bg-gray-400"
                    >
                        {isCommandeEnCours ? "Traitement en cours... ⏳" : "Passer la commande"}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default PanneauPanier;