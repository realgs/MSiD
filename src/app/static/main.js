const create_chart = (handle, data, market) => {
  const div = document.createElement('div');
  div.setAttribute('class', market);
  div.setAttribute('title', market);
  handle.appendChild(div);
  const margin = { top: 50, right: 50, bottom: 50, left: 50 };
  const width = 500;
  const height = 500;
  // add SVG to the page
  const svg = d3
    .select(`.${market}`)
    .append('svg')
    .attr('width', width + margin['left'] + margin['right'])
    .attr('height', height + margin['top'] + margin['bottom'])
  //.call(responsivefy)
    .append('g')
    .attr('transform', `translate(${margin['left']},  ${margin['top']})`);
  // find data range
  const xMin = d3.min(data, d => {
    return d['date'];
  });
  const xMax = d3.max(data, d => {
    return d['date'];
  });
  const yMin = d3.min(data, d => {
    return d['buy'];
  });
  const yMax = d3.max(data, d => {
    return d['sell'];
  });
  // scales for the charts
  const xScale = d3
    .scaleTime()
    .domain([xMin, xMax])
    .range([0, width]);
  const yScale = d3
    .scaleLinear()
    .domain([yMin - 5, yMax])
    .range([height, 0]);
  // create the axes component
  svg
    .append('g')
    .attr('id', 'xAxis')
    .attr('transform', `translate(0, ${height})`)
    .call(d3.axisBottom(xScale));
  svg
    .append('g')
    .attr('id', 'yAxis')
    .attr('transform', `translate(${width}, 0)`)
    .call(d3.axisRight(yScale));

  // generates close price line chart when called
  const buyLine = d3
    .line()
    .x(d => {
      return xScale(d['date']);
    })
    .y(d => {
      return yScale(d['buy']);
    });

  const sellLine = d3
    .line()
    .x(d => {
      return xScale(d['date']);
    })
    .y(d => {
      return yScale(d['sell']);
    });
  // Append the path and bind data
  svg
    .append('path')
    .data([data])
    .style('fill', 'none')
    .attr('id', 'buyChart')
    .attr('stroke', 'steelblue')
    .attr('stroke-width', '1.5')
    .attr('d', buyLine);

  svg
    .append('path')
    .data([data])
    .style('fill', 'none')
    .attr('id', 'sellChart')
    .attr('stroke', 'red')
    .attr('stroke-width', '1.5')
    .attr('d', sellLine);
const bisectDate = d3.bisector(d => d.date).left;
const updateLegends = currentData => {
  d3.selectAll('.lineLegend').remove();
  const legendKeys = Object.keys(data[0]);
  const lineLegend = svg
    .selectAll('.lineLegend')
    .data(legendKeys)
    .enter()
    .append('g')
    .attr('class', 'lineLegend')
    .attr('transform', (d, i) => {
      return `translate(0, ${i * 20})`;
    });
  lineLegend
    .append('text')
    .text(d => {
      if (d === 'date') {
        return `${d}: ${currentData[d].toLocaleDateString()}`;
      } else if (d === 'sell' || d === 'buy') {
        return `${d}: ${currentData[d].toFixed(2)}`;
      } else {
        return `${d}: ${currentData[d]}`;
      }
    })
    .style('fill', 'white')
    .attr('transform', 'translate(15,9)');
  };

  // renders x and y crosshair
  const fClass = `${market}focus`
  const oClass = `${market}overlay`
  const focus = svg
    .append('g')
    .attr('class', fClass)
    .style('display', 'none');
  focus.append('circle').attr('r', 4.5);
  focus.append('line').classed('x', true);
  focus.append('line').classed('y', true);
function generateCrosshair() {
  //returns corresponding value from the domain
  const correspondingDate = xScale.invert(d3.mouse(this)[0]);
  //gets insertion point
  const i = bisectDate(data, correspondingDate, 1);
  const d0 = data[i - 1];
  const d1 = data[i];
  const currentPoint = correspondingDate - d0['date'] > d1['date'] - correspondingDate ? d1 : d0;
  focus.attr('transform',`translate(${xScale(currentPoint['date'])},${yScale(currentPoint['buy'])})`);
focus
  .select('line.x')
  .attr('x1', 0)
  .attr('x2', width - xScale(currentPoint['date']))
  .attr('y1', 0)
  .attr('y2', 0);
focus
  .select('line.y')
  .attr('x1', 0)
  .attr('x2', 0)
  .attr('y1', 0)
  .attr('y2', height - yScale(currentPoint['buy']));
 updateLegends(currentPoint);
}
  svg
    .append('rect')
    .attr('class', oClass)
    .attr('width', width)
    .attr('height', height)
    .on('mouseover', () => focus.style('display', null))
    .on('mouseout', () => focus.style('display', 'none'))
    .on('mousemove', generateCrosshair);
  d3.select(`.${oClass}`).style('fill', 'none');
  d3.select(`.${oClass}`).style('pointer-events', 'all');
  d3.selectAll(`.${fClass} line`).style('fill', 'none');
  d3.selectAll(`.${fClass} line`).style('stroke', '#67809f');
  d3.selectAll(`.${fClass} line`).style('stroke-width', '1.5px');
  d3.selectAll(`.${fClass} line`).style('stroke-dasharray', '3 3');

}
