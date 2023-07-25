import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
const HelloWorld = () => import('@/components/HelloWorld');
const SummaryGenerate = () => import('@/components/SummaryGenerate');
const BatchGenerate = () => import('@/components/BatchGenerate');
const HistoryList = () => import('@/components/HistoryList');
const WordCloud = () => import('@/components/WordCloud');
const AdminVerify = () => import('@/components/AdminVerify');


Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/hello',
            name: 'HelloWorld',
            component: HelloWorld
        },
        {
            path: '/summary_generate',
            name: 'SummaryGenerate',
            component: SummaryGenerate
        },
        {
            path: '/batch_generate',
            name: 'BatchGenerate',
            component: BatchGenerate
        },
        {
            path: '/history_list',
            name: 'HistoryList',
            component: HistoryList
        },
        {
            path: '/word_cloud',
            name: 'WordCloud',
            component: WordCloud
        },
        {
            path: '/verify',
            name: 'AdminVerify',
            component: AdminVerify
        }
    ],

})