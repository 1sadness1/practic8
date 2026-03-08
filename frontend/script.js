const API_URL = 'http://localhost:8000';

let products = [];
let categories = [];


async function loadProducts() {
    const container = document.getElementById('products-container');
    container.innerHTML = '<div class="loading">Загрузка товаров...</div>';
    
    try {
        console.log('Загрузка товаров...');
        const response = await fetch(`${API_URL}/products/all`);
        
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        
        products = await response.json();
        console.log('Товары загружены:', products);
        
        if (products.length === 0) {
            container.innerHTML = '<div class="error">Нет товаров в базе данных</div>';
            return;
        }
        
        renderProducts(products);
    } catch (error) {
        console.error('Ошибка загрузки товаров:', error);
        container.innerHTML = `<div class="error">Не удалось загрузить товары. Проверьте, запущен ли сервер на ${API_URL}</div>`;
    }
}


async function loadCategories() {
    try {
        console.log('Загрузка категорий...');
        const response = await fetch(`${API_URL}/categories/`);
        
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        
        categories = await response.json();
        console.log('Категории загружены:', categories);
        renderCategoryFilter(categories);
    } catch (error) {
        console.error('Ошибка загрузки категорий:', error);
        const select = document.getElementById('category-filter');
        if (select) {
            select.innerHTML = '<option value="">Все категории</option>';
        }
    }
}


async function loadProductById(id) {
    const detailsContainer = document.getElementById('product-details');
    const productsContainer = document.getElementById('products-container');
    const productInfo = detailsContainer.querySelector('.product-info');
    
    productsContainer.style.display = 'none';
    detailsContainer.classList.remove('hidden');
    productInfo.innerHTML = '<div class="loading">Загрузка товара...</div>';
    
    try {
        console.log(`Загрузка товара с ID: ${id}`);
        const response = await fetch(`${API_URL}/products/get/${id}`);
        
        if (!response.ok) {
            throw new Error(`Ошибка HTTP: ${response.status}`);
        }
        
        const product = await response.json();
        console.log('Товар загружен:', product);
        showProductDetails(product);
    } catch (error) {
        console.error('Ошибка загрузки товара:', error);
        productInfo.innerHTML = `<div class="error">Ошибка загрузки товара: ${error.message}</div>`;
    }
}


function renderProducts(productsToRender) {
    const container = document.getElementById('products-container');
    const detailsContainer = document.getElementById('product-details');
    
    container.style.display = 'grid';
    detailsContainer.classList.add('hidden');
    
    let html = '';
    productsToRender.forEach(product => {
        const categoryName = product.category ? product.category.name : 'Без категории';
        const imageUrl = product.image_url || 'https://via.placeholder.com/300x200/2c3e50/ffffff?text=Товар';
        
        html += `
            <div class="product-card" onclick="showProduct(${product.id})">
                <img src="${imageUrl}" alt="${escapeHtml(product.name)}" class="product-image" 
                     onerror="this.src='https://via.placeholder.com/300x200/e74c3c/ffffff?text=Ошибка'">
                <div class="product-info">
                    <h3 class="product-name">${escapeHtml(product.name)}</h3>
                    <div class="product-price">${formatPrice(product.price)} ₽</div>
                    <div class="product-category">${escapeHtml(categoryName)}</div>
                    <div class="product-stock">В наличии: ${product.stock} шт.</div>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}


function showProductDetails(product) {
    const detailsContainer = document.getElementById('product-details');
    const productInfo = detailsContainer.querySelector('.product-info');
    
    const categoryName = product.category ? product.category.name : 'Без категории';
    const imageUrl = product.image_url || 'https://via.placeholder.com/600x400/2c3e50/ffffff?text=Товар';
    const description = product.description || 'Нет описания';
    
    productInfo.innerHTML = `
        <div class="detail-card">
            <img src="${imageUrl}" alt="${escapeHtml(product.name)}" class="detail-image"
                 onerror="this.src='https://via.placeholder.com/600x400/e74c3c/ffffff?text=Ошибка'">
            <div class="detail-info">
                <h2>${escapeHtml(product.name)}</h2>
                <div class="product-category">${escapeHtml(categoryName)}</div>
                <p class="detail-description">${escapeHtml(description)}</p>
                <div class="detail-price">${formatPrice(product.price)} ₽</div>
                <div class="product-stock">В наличии: ${product.stock} шт.</div>
                <button class="back-btn" onclick="backToCatalog()">← Вернуться к каталогу</button>
            </div>
        </div>
    `;
}


function filterByCategory() {
    const categoryId = document.getElementById('category-filter').value;
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    
    let filtered = products;
    
    if (categoryId) {
        filtered = filtered.filter(p => p.category_id == categoryId);
    }
    
    if (searchTerm) {
        filtered = filtered.filter(p => 
            p.name.toLowerCase().includes(searchTerm) || 
            (p.description && p.description.toLowerCase().includes(searchTerm))
        );
    }
    
    renderProducts(filtered);
}


function renderCategoryFilter(categories) {
    const select = document.getElementById('category-filter');
    if (!select) return;
    
    let options = '<option value="">Все категории</option>';
    
    categories.forEach(category => {
        options += `<option value="${category.id}">${escapeHtml(category.name)}</option>`;
    });
    
    select.innerHTML = options;
}


window.showProduct = function(id) {
    loadProductById(id);
};


window.backToCatalog = function() {
    const detailsContainer = document.getElementById('product-details');
    const productsContainer = document.getElementById('products-container');
    
    detailsContainer.classList.add('hidden');
    productsContainer.style.display = 'grid';
};


function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}


function formatPrice(price) {
    return Number(price).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}


document.getElementById('main-link')?.addEventListener('click', (e) => {
    e.preventDefault();
    backToCatalog();
    loadProducts();
});

document.getElementById('categories-link')?.addEventListener('click', (e) => {
    e.preventDefault();
    alert('Функция категорий в разработке');
});

document.getElementById('about-link')?.addEventListener('click', (e) => {
    e.preventDefault();
    alert('Проект "Каталог товаров" создан с использованием FastAPI, SQLite и JavaScript');
});


document.getElementById('search-input')?.addEventListener('input', filterByCategory);


document.getElementById('category-filter')?.addEventListener('change', filterByCategory);


document.addEventListener('DOMContentLoaded', () => {
    console.log('Страница загружена, начинаем загрузку данных...');
    loadProducts();
    loadCategories();
});