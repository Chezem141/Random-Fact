async function getFact() {
    try {
        const response = await fetch('/get_fact');
        const data = await response.json();

        if (data.error) {
            document.getElementById('error').innerHTML = data.error;
            document.getElementById('ai-output').innerHTML = '';
        } else {
            // document.getElementById('ai-output').innerHTML = data.fact.replace(/\*\*(.*?)\*\*/g, '<em>$1</em>');
            document.getElementById('ai-output').innerHTML = marked.parse(data.fact);
            document.getElementById('error').innerHTML = '';
        }
    } catch (err) {
        document.getElementById('error').innerHTML = 'Ошибка при получении факта';
        console.error(err);
    }
}

window.onload = getFact;