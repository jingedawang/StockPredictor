import { Card, Select } from 'antd';
import React, { useEffect } from 'react';
import * as echarts from 'echarts';

import './Query.css';

const { Option } = Select;

export function Query() {
    const onSelect = (value) => {
        console.log('select:', value);
    };
    
    const Stocks = [
        { id: 10013, name: "stock1"},
        { id: 10011, name: "stock2"},
        { id: 20022, name: "stock3"},
        { id: 31213, name: "stock4"},
        { id: 30024, name: "stock5"},
        { id: 43219, name: "stock6"},
        { id: 40090, name: "stock7"},
        { id: 56111, name: "stock8"},
        { id: 56233, name: "stock9"},
        { id: 70028, name: "stock10"},
        { id: 88888, name: "stock11"},
        { id: 10000, name: "stock12"},
        { id: 90000, name: "stock13"}
    ];
    
    const data = [
        {"date": '20210812', "value": '0.37'},
        {"date": '20210813', "value": '0.39'},
        {"date": '20210814', "value": '0.44'},
        {"date": '20210815', "value": '0.53'},
        {"date": '20210816', "value": '0.52'},
        {"date": '20210817', "value": '0.34'},
        {"date": '20210818', "value": '0.60'},
        {"date": '20210819', "value": '0.32'},
        {"date": '20210820', "value": '0.38'},
        {"date": '20210821', "value": '0.35'},
    ];
    
    const column = data && data.map(item => Number(item.value)).sort();
    
    const columnScale = Number(((column[column.length - 1] - column[0]) / 10).toFixed(2));
    
    for(let i = 1; i < 9; i++) {
        column[i] = Number((column[i - 1] + columnScale).toFixed(2));
    }
    
    column[9] = column[column.length - 1]
    
    const scale = {
      value: {
          type: "linear",
        tickCount: 5,
        ticks: column.slice(0, 10),
        }
    };


    
    function Result(props) {
      useEffect(() => {
        const myChart = echarts.init(document.getElementById("charts"));
        myChart.setOption({
          title: {
            text: "",
          },
          tooltip: {},
          xAxis: {
            data: props.data.map((i) => i.date),
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: "price",
              type: "line",
              smooth: true,
              color: "#23CD00",
              data: props.data.map((i) => i.value),
            },
          ],
        });
      }, []);
      return (
        <>
          <div id='charts' style={{width: 800, height: 600 }}/>
        </>
      );
    }

    return (
        <Card className='main'>
            <Select
                style={{ width: 150 }}
                showSearch
                placeholder="Select your stock"
                optionFilterProp="label"
                onSelect={onSelect}
                filterOption={(input, option) => (option.children.toLowerCase().includes(input.toLowerCase()) || option.value.toString().includes(input))}
            >
                { Stocks && Stocks.map(stock => <Option value={stock.id}>{stock.name}</Option>)}
            </Select>
            { data && data.length ? <Result data={data} scale={scale}/> : null }
        </Card>
    );
}