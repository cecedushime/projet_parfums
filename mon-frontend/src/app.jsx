import { useState, useEffect } from 'react';

function App() {
    const [parfums, setParfums] = useState([]);
    const [loading, setLoading] = useState(true);
    // On crée l'état du panier (un tableau vide au départ)
    const [panier, setPanier] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/api/v1/parfums/')
         .then(response => response.json())
         .then(data => {
            setParfums(data.results);
            setLoading(false);
         })
         .catch(error => {
            console.error("Erreur :", error);
            setLoading(false);
         });
    }, []);

    // La fonction pour ajouter un parfum au panier
    const ajouterAuPanier = (parfum) => {
        // On vérifie si le parfum est déjà dans le panier
        const existeDeja = panier.find(item => item.id === parfum.id);
        
        if (existeDeja) {
            // S'il existe, on augmente juste sa quantité
            setPanier(panier.map(item => 
                item.id === parfum.id 
                    ? { ...item, quantite: item.quantite + 1 } 
                    : item
            ));
        } else {
            // Sinon, on l'ajoute avec une quantité de 1
            setPanier([...panier, { ...parfum, quantite: 1 }]);
        }
        
        alert(`🛒 ${parfum.nom} ajouté au panier !`);
    };

    // Calculer le nombre total d'articles (pour le header)
    const totalArticles = panier.reduce((total, item) => total + item.quantite, 0);

    if (loading) {
        return <div className="text-center mt-20 text-2xl font-bold">Chargement des parfums... ⏳</div>;
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-black text-white p-4 shadow-md">
                <div className="container mx-auto flex justify-between items-center">
                    <h1 className="text-2xl font-bold tracking-wider">LUXE PARFUMS</h1>
                    <nav>
                        <a href="#" className="hover:text-yellow-500 mr-4">Accueil</a>
                        <a href="#" className="hover:text-yellow-500 mr-4">Boutique</a>
                        {/* 👇 Le compteur du panier est maintenant dynamique */}
                        <a href="#" className="hover:text-yellow-500 font-bold">
                            Panier ({totalArticles})
                        </a>
                    </nav>
                </div>
            </header>

            {/* Contenu principal */}
            <main className="container mx-auto p-8">
                <h2 className="text-3xl font-semibold mb-8 text-gray-800">Notre Collection</h2>
                
                {parfums.length === 0 ? (
                    <p className="text-gray-500">Aucun parfum trouvé.</p>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {parfums.map(parfum => (
                            <div key={parfum.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition duration-300">
                                <div className="h-48 bg-gray-200 flex items-center justify-center text-gray-500">
                                    [Image du parfum]
                                </div>
                                
                                <div className="p-6">
                                    <h3 className="text-xl font-bold mb-2 text-gray-900">{parfum.nom}</h3>
                                    <p className="text-gray-600 mb-4">{parfum.marque}</p>
                                    
                                    <div className="flex justify-between items-center mt-4">
                                        <span className="text-2xl font-bold text-black">{parfum.prix} AED</span>
                                        {/* 👇 On ajoute l'événement onClick sur le bouton */}
                                        <button 
                                            onClick={() => ajouterAuPanier(parfum)}
                                            className="bg-black text-white px-4 py-2 rounded hover:bg-gray-800 transition active:scale-95"
                                        >
                                            Ajouter
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;