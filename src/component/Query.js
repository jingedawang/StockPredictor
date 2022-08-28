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
      {
          id: "600479",
          pinyin: "QJYY",
          name: "千金药业"
      },
      {
          id: "600480",
          pinyin: "LYGF",
          name: "凌云股份"
      },
      {
          id: "600481",
          pinyin: "SLJN",
          name: "双良节能"
      }
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
        {"date": '20210831', "value": '0.51'},
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
      const length = data.length;
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
          visualMap: {
            show: false,
            dimension: 0,
            pieces: [
              {
                lte: 1,
                color: "#23CD00"
              },
              {
                gt: 1,
                lte: length - 2,
                color: "#23CD00"
              },
              {
                gt: length - 2,
                color: 'red',
              }
            ]
          },
          series: [
            {
              name: "price",
              type: "line",
              smooth: true,
              data: props.data.map((i) => i.value),
              markArea: {
                itemStyle: {
                  color: 'rgba(255, 173, 177, 0.4)'
                },
                data: [
                  [
                    {
                      name: 'Forecast after Two Weeks',
                      xAxis: data[length - 2].date
                    },
                    {
                      xAxis: data[length - 1].date
                    }
                  ]
                ]
              }
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
                filterOption={(input, option) => (option.value.toLowerCase().includes(input.toLowerCase()) || option.children.includes(input)) }
            >
                { Stocks && Stocks.map(stock => <Option value={stock.pinyin} key={stock.id}>{stock.name}</Option>)}
            </Select>
            { data && data.length ? <Result data={data} scale={scale}/> : null }
        </Card>
    );
}