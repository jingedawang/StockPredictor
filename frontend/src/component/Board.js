import { Card, Table, Tag } from 'antd';
import React, { useEffect, useState } from 'react';

import './Board.css';

const columns = [
    {
        title: 'Name of Stock',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: 'Id of Stock',
        dataIndex: 'id',
        key: 'id',
    },
    {
        title: 'Price Change after Two Weeks',
        dataIndex: 'rate',
        key: 'rate',
        render: (rate, _, idx) => (
            <>              
                {rate ? <Tag color={rate > 0 ? "red" : "green"} key={idx}>
                    {`${(Number(rate) * 100).toFixed(2)}%`}
                </Tag> : null}            
            </>
        )
    }
];


export function Board() {
    const [data, setData] = useState([]);
    useEffect(() => {
        const tmp = [];
        const key = localStorage.getItem("key").split(",");
        for ( let i = key.length - 1; i >= Math.max(0, key.length - 10); i-- ) {
            tmp.push(JSON.parse(localStorage.getItem(key[i])));
        }
        setData(tmp);
    },[data]);
    return (
        <Card className='main'>
            <Table columns={columns} dataSource={data}/>
        </Card>
    );
}