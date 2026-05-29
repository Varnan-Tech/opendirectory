/**
 * Company Radar heat score calculator.
 * 4 dimensions (Authority, Shipping, Social, Growth), each max 25, total 0-100.
 * Usage: node heat-score-calc.mjs --file signals.json
 * Input: JSON with companies[] containing signal fields.
 * Output: JSON with scored results, dimension breakdowns, and alerts.
 */

import { readFileSync } from 'fs';

function scoreAuthority(signals) {
  const stars = Number(signals.stars) || 0;
  const forks = Number(signals.forks) || 0;
  const phVotes = Number(signals.ph_votes) || 0;
  const breakdown = {
    stars: Math.min(15, (stars / 1000) * 3),
    forks: Math.min(5, (forks / 200) * 2),
    ph_votes: Math.min(5, (phVotes / 100) * 5)
  };
  const total = breakdown.stars + breakdown.forks + breakdown.ph_votes;
  return { score: Math.min(25, total), max: 25, breakdown };
}

function scoreShipping(signals) {
  const commits = Number(signals.commits_week) || 0;
  const releases = Number(signals.releases_month) || 0;
  const daysSince = signals.last_activity_days ?? 999;
  const breakdown = {
    commits_week: Math.min(10, commits * 2),
    releases_month: releases > 0 ? 5 : 0,
    active_shipping: signals.active_shipping === true ? 5 : 0,
    recency: daysSince < 7 ? 5 : (daysSince < 30 ? 3 : 0)
  };
  const total = breakdown.commits_week + breakdown.releases_month + breakdown.active_shipping + breakdown.recency;
  return { score: Math.min(25, total), max: 25, breakdown };
}

function scoreSocial(signals) {
  const breakdown = {
    tweets_24h: Math.min(5, (Number(signals.tweets_24h) || 0) * 1),
    mentions: Math.min(5, (Number(signals.mentions) || 0) * 2),
    reddit_posts: Math.min(3, (Number(signals.reddit_posts) || 0) * 1.5),
    reddit_score: Math.max(0, Math.min(2, ((Number(signals.reddit_score) || 0) / 100) * 2)),
    hn_stories: Math.min(4, (Number(signals.hn_stories) || 0) * 2),
    hn_points: Math.min(3, ((Number(signals.hn_points) || 0) / 200) * 3),
    youtube_videos: Math.min(3, (Number(signals.youtube_videos) || 0) * 1)
  };
  const total = Object.values(breakdown).reduce((a, b) => a + b, 0);
  return { score: Math.min(25, total), max: 25, breakdown };
}

function scoreGrowth(signals) {
  const breakdown = {
    jobs: Math.min(10, (Number(signals.jobs) || 0) * 3),
    dept_diversity: Math.min(5, (Number(signals.dept_count) || 0) * 2),
    ai_sentiment: Math.min(5, ((Number(signals.sentiment) || 0) / 100) * 5),
    ai_traction: Math.min(5, ((Number(signals.traction) || 0) / 100) * 5)
  };
  const total = Object.values(breakdown).reduce((a, b) => a + b, 0);
  return { score: Math.min(25, total), max: 25, breakdown };
}

function activityLevel(score) {
  if (score >= 60) return 'High';
  if (score >= 30) return 'Medium';
  if (score >= 1) return 'Low';
  return 'Dormant';
}

function generateAlerts(name, dims, signals) {
  const alerts = [];
  if ((Number(signals.jobs) || 0) >= 5)
    alerts.push({ type: 'hiring_spike', severity: 'medium', message: `${name} has ${signals.jobs} open roles` });
  if ((Number(signals.tweets_24h) || 0) >= 20)
    alerts.push({ type: 'high_tweet_volume', severity: 'medium', message: `${name} tweeted ${signals.tweets_24h} times in 24h` });
  if ((Number(signals.commits_week) || 0) >= 30)
    alerts.push({ type: 'high_shipping_velocity', severity: 'low', message: `${name} shipped ${signals.commits_week} commits this week` });
  if (dims.social.score >= 20)
    alerts.push({ type: 'strong_social_presence', severity: 'low', message: `${name} has high social engagement (${Math.round(dims.social.score)}/25)` });
  if (dims.growth.score >= 20)
    alerts.push({ type: 'strong_growth_signals', severity: 'medium', message: `${name} shows strong growth signals (${Math.round(dims.growth.score)}/25)` });
  return alerts;
}

function computeCompany(company) {
  const { name, signals } = company;
  if (!signals) return { name, heat_score: 0, level: 'Dormant', dimensions: { authority: {score:0,max:25,breakdown:{}}, shipping: {score:0,max:25,breakdown:{}}, social: {score:0,max:25,breakdown:{}}, growth: {score:0,max:25,breakdown:{}} }, alerts: [] };
  const authority = scoreAuthority(signals);
  const shipping = scoreShipping(signals);
  const social = scoreSocial(signals);
  const growth = scoreGrowth(signals);

  const total = Math.round(authority.score + shipping.score + social.score + growth.score);
  return {
    name,
    heat_score: total,
    level: activityLevel(total),
    dimensions: { authority, shipping, social, growth },
    alerts: generateAlerts(name, { authority, shipping, social, growth }, signals)
  };
}

function parseInput(raw) {
  try { return JSON.parse(raw); }
  catch { console.error('Invalid JSON input'); process.exit(1); }
}

function main() {
  const args = process.argv.slice(2);
  const fileIndex = args.indexOf('--file');

  if (fileIndex !== -1 && args[fileIndex + 1]) {
    let raw; try { raw = readFileSync(args[fileIndex + 1], 'utf-8'); } catch (e) { console.error('Cannot read file: ' + args[fileIndex + 1] + ' (' + e.message + ')'); process.exit(1); } const input = parseInput(raw);
    const companies = input.companies || [input];
    const result = {
      generated_at: new Date().toISOString(),
      company_count: companies.length,
      companies: companies.map(computeCompany)
    };
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  } else if (!process.stdin.isTTY) {
    const chunks = [];
    process.stdin.on('data', chunk => chunks.push(chunk));
    process.stdin.on('end', () => {
      const input = parseInput(Buffer.concat(chunks).toString('utf-8'));
      const companies = input.companies || [input];
      const result = {
        generated_at: new Date().toISOString(),
        company_count: companies.length,
        companies: companies.map(computeCompany)
      };
      process.stdout.write(JSON.stringify(result, null, 2) + '\n');
    });
  } else {
    console.error('Usage: node heat-score-calc.mjs --file <input.json>');
    console.error('   or: cat signals.json | node heat-score-calc.mjs');
    process.exit(1);
  }
}

main();
