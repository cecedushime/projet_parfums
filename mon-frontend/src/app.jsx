import { useState, useEffect } from 'react';
import Header from './components/header';
import CarteParfum from './components/carteParfum';
import PanneauPanier from './components/cartePanier';

function App() {
    const [parfums, setParfums] = useState([]);
    const [loading, setLoading] = useState(true);
    const [panier, setPanier] = useState([]);
    const [isPanierOpen, setIsPanierOpen] = useState(false);

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

    const ajouterAuPanier = (parfum) => {
        const existeDeja = panier.find(item => item.id === parfum.id);
        if (existeDeja) {
            setPanier(panier.map(item => 
                item.id === parfum.id ? { ...item, quantite: item.quantite + 1 } : item
            ));
        } else {
            setPanier([...panier, { ...parfum, quantite: 1 }]);
        }
    };

    const supprimerDuPanier = (id) => {
        setPanier(panier.filter(item => item.id !== id));
    };

    const totalArticles = panier.reduce((total, item) => total + item.quantite, 0);

    if (loading) {
        return <div className="text-center mt-20 text-2xl font-bold">Chargement des parfums... ⏳</div>;
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* On appelle notre composant Header */}
            <Header 
                totalArticles={totalArticles} 
                onOuvrirPanier={() => setIsPanierOpen(true)} 
            />

            <main className="container mx-auto p-8">
                <h2 className="text-3xl font-semibold mb-8 text-gray-800">Notre Collection</h2>
                
                {parfums.length === 0 ? (
                    <p className="text-gray-500">Aucun parfum trouvé.</p>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {parfums.map(parfum => (
                            <CarteParfum 
                                key={parfum.id} 
                                parfum={parfum} 
                                onAjouter={ajouterAuPanier} 
                            />
                        ))}
                    </div>
                )}
            </main>

            {/* On appelle notre composant PanneauPanier si ouvert */}
            {isPanierOpen && (
                <PanneauPanier 
                    panier={panier} 
                    onFermer={() => setIsPanierOpen(false)}
                    onSupprimer={supprimerDuPanier}
                />
            )}
        </div>
    );
}

export default App;