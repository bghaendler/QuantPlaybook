import React, { useState, useEffect, useRef } from 'react';
import { MODELS, CATEGORIES } from '../config/models';
import './TopNav.css';
import { ChevronDown } from 'lucide-react';

const TopNav = ({ selectedModel, onSelectModel }) => {
    const [activeCategory, setActiveCategory] = useState(null);
    const navRef = useRef(null);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (navRef.current && !navRef.current.contains(event.target)) {
                setActiveCategory(null);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const handleCategoryClick = (categoryCode) => {
        setActiveCategory(activeCategory === categoryCode ? null : categoryCode);
    };

    // Helper to shorten category names for the top bar if needed
    const getShortLabel = (label) => {
        return label.replace(/^\d+\.\s*/, ''); // Remove "1. ", "2. ", etc.
    };

    return (
        <nav className="top-nav" ref={navRef}>
            <ul className="nav-categories">
                {Object.entries(CATEGORIES).map(([code, label]) => (
                    <li key={code} className={`nav-item ${activeCategory === code ? 'active' : ''}`}>
                        <button
                            className={`nav-link ${Object.values(MODELS).find(m => m.id === selectedModel)?.category === code ? 'current-category' : ''}`}
                            onClick={() => handleCategoryClick(code)}
                        >
                            {getShortLabel(label)}
                            <ChevronDown size={14} className={`chevron ${activeCategory === code ? 'rotate' : ''}`} />
                        </button>

                        {activeCategory === code && (
                            <div className="nav-dropdown">
                                {Object.values(MODELS)
                                    .filter(m => m.category === code)
                                    .map(m => (
                                        <button
                                            key={m.id}
                                            className={`dropdown-item ${selectedModel === m.id ? 'selected' : ''}`}
                                            onClick={() => {
                                                onSelectModel(m.id);
                                                setActiveCategory(null);
                                            }}
                                        >
                                            {m.name}
                                        </button>
                                    ))}
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        </nav>
    );
};

export default TopNav;
