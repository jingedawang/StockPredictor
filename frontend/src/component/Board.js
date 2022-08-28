import { Card, Table, Tag } from 'antd';
import React from 'react';

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
                <Tag color={rate > 0 ? "red" : "green"} key={idx}>
                    {`${rate * 100}%`}
                </Tag>             
            </>
        )
    }
];

const data = [
    {
        key: '1',
        name: 'stock1',
        id: 10013,
        rate: 0.01
    },
    {
        key: '2',
        name: 'stock5',
        id: 30024,
        rate: -0.04
    },
    {
        key: '3',
        name: 'stock13',
        id: 90000,
        rate: 0.13
    },
    {
        key: '4',
        name: 'stock11',
        id: 88888,
        rate: 0.02
    },
    {
        key: '5',
        name: 'stock10',
        id: 70028,
        rate: 0.06
    },
    {
        key: '6',
        name: 'stock8',
        id: 56111,
        rate: 0.09
    },
    {
        key: '7',
        name: 'stock7',
        id: 40090,
        rate: 0.10
    }
];

export function Board() {
    return (
        <Card className='main'>
            <Table columns={columns} dataSource={data}/>
        </Card>
    );
}