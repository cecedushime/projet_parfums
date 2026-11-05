function Header({ totalArticles, onOuvrirPanier }) {
    return (
        <header className="bg-black text-white p-4 shadow-md">
            <div className="container mx-auto flex justify-between items-center">
                <h1 className="text-2xl font-bold tracking-wider">LUXE PARFUMS</h1>
                <nav className="flex items-center space-x-6">
                    <a href="#" className="hover:text-yellow-500">Accueil</a>
                    <a href="#" className="hover:text-yellow-500">Boutique</a>
                    <button 
                        onClick={onOuvrirPanier}
                        className="hover:text-yellow-500 font-bold bg-gray-800 px-4 py-2 rounded transition"
                    >
                        Panier ({totalArticles})
                    </button>
                </nav>
            </div>
        </header>
    );
}

export default Header;