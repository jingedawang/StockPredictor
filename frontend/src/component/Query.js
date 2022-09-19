import { Card, Select } from 'antd';
import React, { useEffect, useState } from 'react';
import * as echarts from 'echarts';
import axios from 'axios';

import './Query.css';

const { Option } = Select;
let charts = undefined;

export function Query() {
    const onSelect = (id) => {
      console.log("###", id)
      axios.get(`http://20.205.61.210:5000/stock/${id}`).then((res) => {
        const result = res.data.history.map(item => ({
          date: Object.keys(item)[0].replaceAll('-', ''),
          value: Object.values(item)[0]
        }))
        result.push({
          date: Object.keys(res.data.predict)[0].replaceAll('-', ''),
          value: Object.values(res.data.predict)[0]
        })
        setPredictData(result);
      });
    };

    const [stocksList, setStocksList] = useState([]);
    const [predictData, setPredictData] = useState([]);

    useEffect(() => {
      axios.get("http://20.205.61.210:5000/stock/list").then((res) => {
        setStocksList(res.data);
      })
    },[]);
    
    function Result(props) {
      const length = props.data.length;
      useEffect(() => {
        const options = {
          title: {
            text: "",
          },
          tooltip: {},
          xAxis: {
            data: props.data.map((i) => i.date),
          },
          yAxis: {
            type: "value",
            min: Math.min(...props.data.map((i) => i.value)),
            max: Math.max(...props.data.map((i) => i.value)),
            axisLabel: {
              formatter: '{value}'
            }
          },
          visualMap: {
            show: false,
            dimension: 0,
            pieces: [
              {
                lte: 1,
                color: "#23CD00",
              },
              {
                gt: 1,
                lte: length - 2,
                color: "#23CD00",
              },
              {
                gt: length - 2,
                color: "red",
              },
            ],
          },
          series: [
            {
              name: "price",
              type: "line",
              smooth: true,
              data: props.data.map((i) => i.value),
              markArea: {
                itemStyle: {
                  color: "rgba(255, 173, 177, 0.4)",
                },
                data: [
                  [
                    {
                      name: "Forecast after Two Weeks",
                      xAxis: props.data[length - 2].date,
                    },
                    {
                      xAxis: props.data[length - 1].date,
                    },
                  ],
                ],
              },
            },
          ],
        };
        charts = echarts.init(document.getElementById("charts"));
        charts.setOption(options);
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
                filterOption={(input, option) => (option.key.toLowerCase().includes(input.toLowerCase()) || option.children.includes(input)) }
            >
                { stocksList && stocksList.map(stock => <Option key={stock.pinyin} value={stock.id}>{stock.name}</Option>)}
            </Select>
            { predictData && predictData.length ? <Result data={predictData}/> : null }
        </Card>
    );
}