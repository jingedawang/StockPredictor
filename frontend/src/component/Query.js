import { Alert, Card, Select } from 'antd';
import React, { useEffect, useState } from 'react';
import * as echarts from 'echarts';
import axios from 'axios';

import './Query.css';

const { Option } = Select;
let charts = undefined;
const key = [];

export function Query() {
    const [select, setSelect] = useState(0);
    const onSelect = (id) => {
      axios.get(`http://20.205.61.210:5000/stock/${id}`).then((res) => {
        if(res.data.history && res.data.history.length && Object.values(res.data.predict) && Object.values(res.data.predict).length) {
          const result = res.data.history.map(item => ({
            date: Object.keys(item)[0].replaceAll('-', ''),
            value: Object.values(item)[0]
          }))
          result.push({
            date: Object.keys(res.data.predict)[0].replaceAll('-', ''),
            value: Object.values(res.data.predict)[0]
          })
          setPredictData(result);
          const data = {
            key: res.data.id,
            name: res.data.name,
            id: res.data.id,
            rate: (Object.values(res.data.predict)[0] - Object.values(res.data.history[res.data.history.length - 1])[0]) / Object.values(res.data.history[res.data.history.length - 1])[0]
          }
          if (!localStorage.getItem(res.data.id)) {
            localStorage.setItem(res.data.id, JSON.stringify(data));
          }
          if (key.indexOf(res.data.id) !== -1) {
            let idx = key.indexOf(res.data.id);
            key.splice(idx, 1);
          }
          key.push(res.data.id);
          localStorage.setItem("key", key);
          setSelect(1);
          return;
        }
        setSelect(-1);
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
                silent: true,
                itemStyle: {
                  color: "rgba(255, 173, 177, 0.4)",
                },
                data: [
                  [
                    {
                      xAxis: props.data[length - 2].date,
                      label: {
                        position: 'left',
                      },
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
        window.onresize = function() {
          charts.resize();
        };
      }, []);
      return (
        <>
          <div id='charts'/>
        </>
      );
    }

    function AlertMsg() {
      return (
        <Alert
          message="Error"
          description="No current stock information found."
          type="error"
          showIcon
        />
      )
    }

    function Charts() {
      if (!select && !predictData?.length) {
        return null;
      } 
      return select > 0 ? <Result data={predictData}/> : <AlertMsg />
    }

    return (
        <Card className='main'>
            <Select
                className='select'
                showSearch
                placeholder="Select your stock"
                optionFilterProp="label"
                onSelect={onSelect}
                filterOption={(input, option) => (option['data-pinyin'].toLowerCase().includes(input.toLowerCase()) || option.children.includes(input))}
            >
                { stocksList && stocksList.map((stock, idx) => <Option key={idx} value={stock.id} data-pinyin={stock.pinyin}>{stock.name}</Option>)}
            </Select>
            <Charts className='chart'/>
        </Card>
    );
}