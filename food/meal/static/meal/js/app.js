function transliterate(text) {
    const map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu',
        'я': 'ya', ' ': '-', '–': '-', '—': '-', '_': '-'
    };

    return text
        .toLowerCase()
        .split('')
        .map(char => map[char] || char)
        .join('')
        .replace(/[^a-z0-9-]+/g, '')
        .replace(/--+/g, '-')
        .replace(/^-+|-+$/g, '');
}

document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    const isAddPage = path === '/addpage/';
    const isEditPage = path.startsWith('/edit/');

    if (isAddPage || isEditPage) {
        const titleInput = document.querySelector('#id_title');
        const slugInput = document.querySelector('#id_slug');

        if (titleInput && slugInput) {
            titleInput.addEventListener('input', () => {
                slugInput.value = transliterate(titleInput.value);
            });
        }
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const toasts = document.querySelectorAll(".toast");

    toasts.forEach((toast) => {
        toast.style.display = "block";
        toast.style.opacity = "0";
        toast.style.transition = "opacity 1s ease-in-out";

        setTimeout(() => {
            toast.style.opacity = "1";
        }, 10);

        setTimeout(() => {
            toast.style.opacity = "0";
            setTimeout(() => {
                toast.style.display = "none";
            }, 1000);
        }, 5000);

        const closeButton = toast.querySelector(".btn-close");
        if (closeButton) {
            closeButton.addEventListener("click", () => {
                toast.style.opacity = "0";
                setTimeout(() => {
                    toast.style.display = "none";
                }, 1000);
            });
        }
    });
});
