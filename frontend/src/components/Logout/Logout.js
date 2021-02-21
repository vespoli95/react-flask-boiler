 
 export default function Logout({ token, setToken }){

    const handleSubmit = async e => {
        e.preventDefault();
        sessionStorage.clear(token);
        setToken("");
    } 
    return (
        <form onSubmit={handleSubmit}>
            <button type="submit">Logout</button>
        </form>
    );
}
 
