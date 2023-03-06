import { Card, Table } from 'antd';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

import './Recommend.css';

const columns = [
    {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
    },
    {
        title: 'Id',
        dataIndex: 'id',
        key: 'id',
    },
    {
        title: 'Increase',
        dataIndex: 'increase',
        key: 'increase',
    }
];

export function Recommend() {
    const [data, setData] = useState([]); 

    useEffect(() => {
        axios.get("http://stockprediction.org:5000/stock/top5").then((res) => {
            setData(res.data);
        })
      },[]);
    return (
        <Card className='recommend' title="Recommend Top 5">
            <Table columns={columns} dataSource={data} pagination={false} />
        </Card>
    );
}