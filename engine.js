(function (root) {
  "use strict";
  var SPANS = [
    { cap: 7, span: 76, verdict: "a reading nook" },
    { cap: 13, span: 107, verdict: "a bedroom" },
    { cap: 23, span: 132, verdict: "a living room" },
    { cap: 37, span: 152, verdict: "a great room" }
  ];
  var BODY = 30;    // labeled fan body drop, cm
  var TARGET = 240; // labeled target blade height, cm
  var MINCEIL = 240; // labeled minimum ceiling for a fan, cm
  var COVER = 37;   // labeled m2 one 152 cm fan can stir

  function round1(x) { return Math.round(x * 10) / 10; }
  function plural(n, word) { return n + " " + word + (n === 1 ? "" : "s"); }

  function spanPlan(lenM, widM) {
    if (!(lenM > 0) || !(widM > 0)) return { error: "the room sides must be positive" };
    var area = round1(lenM * widM);
    var span = 152, verdict = "a great room that wants two fans";
    for (var i = 0; i < SPANS.length; i++) {
      if (area <= SPANS[i].cap) { span = SPANS[i].span; verdict = SPANS[i].verdict; break; }
    }
    return { area: area, span: span, verdict: verdict };
  }

  function rodPlan(ceilingCm) {
    if (!(ceilingCm > 0)) return { error: "the ceiling height must be positive" };
    if (ceilingCm < MINCEIL) return { error: "the ceiling is below the labeled 240 cm minimum for a fan" };
    var rod = round1(Math.max(0, ceilingCm - BODY - TARGET));
    var verdict;
    if (rod === 0) verdict = "no room for a downrod";
    else if (rod <= 15) verdict = "a short drop";
    else if (rod <= 90) verdict = "a standard drop";
    else verdict = "a long drop for a tall ceiling";
    return { rod: rod, verdict: verdict };
  }

  function countPlan(lenM, widM) {
    if (!(lenM > 0) || !(widM > 0)) return { error: "the room sides must be positive" };
    var area = round1(lenM * widM);
    var count = Math.max(1, Math.ceil(area / COVER));
    var longWall = round1(Math.max(lenM, widM));
    var spacing = round1(longWall / count);
    var verdict;
    if (count === 1) verdict = "one fan covers it";
    else if (count <= 3) verdict = "a row of fans";
    else verdict = "a grid of fans";
    return { area: area, count: count, spacing: spacing, longWall: longWall, verdict: verdict };
  }

  function renderSpan(r, lenM, widM) {
    return "A room " + lenM + " m by " + widM + " m is " + r.area + " m2 - a labeled "
      + r.span + " cm blade span for " + r.verdict + ".";
  }

  function renderRod(r, ceilingCm) {
    var mount = r.rod === 0 ? "a flush mount" : "a labeled " + r.rod + " cm downrod";
    return "A ceiling " + ceilingCm + " cm high takes " + mount + " - " + r.verdict + ".";
  }

  function renderCount(r) {
    var where = r.count === 1
      ? "centered at " + r.spacing + " m on the " + r.longWall + " m wall"
      : "spaced " + r.spacing + " m along the " + r.longWall + " m wall";
    return plural(r.count, "fan") + " for " + r.area + " m2, " + where + " - " + r.verdict + ".";
  }

  var api = { spanPlan: spanPlan, rodPlan: rodPlan, countPlan: countPlan, renderSpan: renderSpan, renderRod: renderRod, renderCount: renderCount };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.FanFit = api;
})(this);
