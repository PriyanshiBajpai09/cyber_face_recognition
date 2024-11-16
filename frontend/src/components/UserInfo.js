import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UserInfo = () => {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        const fetchUsers = async () => {
            const response = await axios.get('http://127.0.0.1:5000/users');
            setUsers(response.data);
        };
        fetchUsers();
    }, []);

    return (
        <div>
            <h2>User Information</h2>
            <ul>
                {users.map(user => (
                    <li key={user.id}>{user.name}</li>
                ))}
            </ul>
        </div>
    );
};

export default UserInfo;