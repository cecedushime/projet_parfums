import { useState, useEffect } from 'react';
import Header from './components/header';
import CarteProduit from './components/carteProduit';
import PanneauPanier from './components/cartePanier';

function App() {
    const [produits, setProduits] = useState([]);
    const [loading, setLoading] = useState(true);
    const [panier, setPanier] = useState([]);
    const [isPanierOpen, setIsPanierOpen] = useState(false);
    const [isCommandeEnCours, setIsCommandeEnCours] = useState(false);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/api/v1/produits/')
         .then(response => response.json())
         .then(data => {
            setProduits(data.results); 
            setLoading(false);
         })
         .catch(error => {
            console.error("Erreur :", error);
            setLoading(false);
         });
    }, []);

    const ajouterAuPanier = (produit) => {
        const existeDeja = panier.find(item => item.id === produit.id);
        if (existeDeja) {
            setPanier(panier.map(item => 
                item.id === produit.id ? { ...item, quantite: item.quantite + 1 } : item
            ));
        } else {
            setPanier([...panier, { ...produit, quantite: 1 }]);
        }
    };

    const supprimerDuPanier = (id) => {
        setPanier(panier.filter(item => item.id !== id));
    };

    const passerCommande = async () => {
        setIsCommandeEnCours(true);
        
        const commandeData = {
            panier: panier.map(item => ({ id: item.id, quantite: item.quantite }))
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/api/v1/commandes/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify(commandeData)
            });

            const data = await response.json();

            if (response.ok) {
                alert("🎉 Commande réussie ! Merci pour votre achat.");
                setPanier([]);
                setIsPanierOpen(false);
            } else {
                alert(`Erreur : ${data.error || 'Problème lors de la commande'}`);
            }
        } catch (error) {
            console.error("Erreur réseau :", error);
            alert("Impossible de contacter le serveur.");
        } finally {
            setIsCommandeEnCours(false);
        }
    };

    const totalArticles = panier.reduce((total, item) => total + item.quantite, 0);

    if (loading) {
        return <div className="text-center mt-20 text-2xl font-bold">Chargement des produits... ⏳</div>;
    }

    return (
        <div className="min-h-screen bg-gray-50">
            <Header 
                totalArticles={totalArticles} 
                onOuvrirPanier={() => setIsPanierOpen(true)} 
            />

            <main className="container mx-auto p-8">
                <h2 className="text-3xl font-semibold mb-8 text-gray-800">Nos Produits High-Tech</h2>
                
                {produits.length === 0 ? (
                    <p className="text-gray-500">Aucun produit trouvé.</p>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {produits.map(produit => (
                            <CarteProduit 
                                key={produit.id} 
                                produit={produit} 
                                onAjouter={ajouterAuPanier} 
                            />
                        ))}
                    </div>
                )}
            </main>

            {isPanierOpen && (
                <PanneauPanier 
                    panier={panier} 
                    onFermer={() => setIsPanierOpen(false)}
                    onSupprimer={supprimerDuPanier}
                    onCommander={passerCommande}
                    isCommandeEnCours={isCommandeEnCours}
                />
            )}
        </div>
    );
}

export default App;