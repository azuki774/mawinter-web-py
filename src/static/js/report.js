async function sample() {
    try {
        const res = await axios.get('https://jsonplaceholder.typicode.com/todos/1');
        const items = JSON.parse(JSON.stringify(res.data));
        testpln.innerHTML = items['id']
        console.log(items)
    } catch (err) {
        console.error(err);
    }
}
