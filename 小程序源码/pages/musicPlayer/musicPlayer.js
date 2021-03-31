var innerAudioContext = wx.createInnerAudioContext();
var wxCharts = require('../../utils/wxcharts.js');
const app = getApp()

Page({
  data: {
    playing: false,
    rank: null,
    language: null,
    emotion: null,
    bpm: null,
    public_time: null,
    genre: null,
    attitude: null,
    name: '未知',
    attitudeInfo: '未知',
    bpmInfo: '未知',
    emotionInfo: '未知',
    genreInfo: '未知',
    languageInfo: '未知',
    like_time: '未知',
    match: '未知',
    unlike_time: '未知',
    public_timeInfo: '未知',
    index: null,
    dianzancnt: 1,
    diancaicnt: 1,
    cainacnt: 1,
    accept: false,
    zan: false,
    cai: false,
    goodsType: '',
    filename: ''
  },
  onLoad: function (options) {
    var that = this
    innerAudioContext = wx.createInnerAudioContext()
    console.log(options)
    that.setData({
      rank: options['rank'],
      language: options['language'],
      emotion: options['emotion'],
      bpm: options['bpm'],
      public_time: options['public_time'],
      genre: options['genre'],
      attitude: options['attitude'],
      name: options['name'],
      attitudeInfo: options['attitudeInfo'],
      bpmInfo: options['bpmInfo'],
      emotionInfo: options['emotionInfo'],
      genreInfo: options['genreInfo'],
      languageInfo: options['languageInfo'],
      like_time: options['like_time'],
      match: options['match'],
      unlike_time: options['unlike_time'],
      public_timeInfo: options['public_timeInfo'],
      index: options['index'],
      goodsType: options['goodsType'],
      error: false,
      filename: options['filename']
    })
    var windowWidth = '', windowHeight = '';    //定义宽高
    try {
      var res = wx.getSystemInfoSync();    //试图获取屏幕宽高数据
      windowWidth = res.windowWidth / 750 * 690;  //以设计图750为主进行比例算换
      windowHeight = res.windowWidth / 750 * 550    //以设计图750为主进行比例算换
    } catch (e) {
      console.error('getSystemInfoSync failed!');  //如果获取失败
    }

    new wxCharts({
      canvasId: 'radarCanvas',
      type: 'radar',
      categories: ['语种', '情感', '节奏', '年代', '流派', '倾向'],
      series: [{
        name: '维度得分',
        data: [7 - this.data.language, 7 - this.data.emotion, 7 - this.data.bpm, 7 - this.data.public_time, 7 - this.data.genre, 7 - this.data.attitude]
      }],
      width: 300,
      height: 300,
      extra: {
        radar: {
          max: 7
        }
      }
    });
  },
  backToPast: function(e) {
    wx.navigateBack({
      delta: 0,
    })
  },
  onMusic: function(e) {
    console.log(innerAudioContext.src)
    if(this.data.error) {
      wx.showModal({
        title: '该音乐为付费项目，暂不支持在线播放！',
        showCancel: false,
        confirmText: '确定'
      })
      return
    }
    if(innerAudioContext.src.length == 0) {
      innerAudioContext.autoplay = true
      innerAudioContext.src = "https://nandodu-blog.oss-cn-shanghai.aliyuncs.com/" + encodeURIComponent('抖音音频数据库') + '/' + encodeURIComponent(this.data.filename) + '.wav'
      innerAudioContext.play()
    } else {
      innerAudioContext.play()
    }
    innerAudioContext.onPlay(() => {
      console.log('开始播放');
      this.setData({
        playing: true
      })
    })
    innerAudioContext.onError((res) => {
      console.log('播放音频失败' + res);
      this.setData({
        error: true
      })
      wx.showModal({
        title: '该音乐为付费项目，暂不支持在线播放！',
        showCancel: false,
        confirmText: '确定'
      })
    })
  },
  pauseMusic: function(e) {
    innerAudioContext.pause();
    innerAudioContext.onPause(() => {
      console.log('暂停播放');
      this.setData({
        playing: false
      })
    })
  },
  stopMusic() {
    innerAudioContext.stop()
    innerAudioContext = wx.createInnerAudioContext()
    this.data.playing = true
    this.onMusic()
  },
  dianzan: function(e) {
    if(!this.data.zan) {
      this.setData({
        zan: true
      })
      app.globalData.items[this.data.index]['like_time'] = parseInt(app.globalData.items[this.data.index]['like_time']) + 1
    } else {
      this.setData({
        zan: false
      })
      app.globalData.items[this.data.index]['like_time'] = parseInt(app.globalData.items[this.data.index]['like_time']) - 1
    }
  },
  diancai: function(e) {
    if(!this.data.cai) {
      this.setData({
        cai: true
      })
      app.globalData.items[this.data.index]['unlike_time'] = parseInt(app.globalData.items[this.data.index]['unlike_time']) + 1
    } else {
      this.setData({
        cai: false
      })
      app.globalData.items[this.data.index]['unlike_time'] = parseInt(app.globalData.items[this.data.index]['unlike_time']) - 1
    }
  },
  caina: function(e) {
    if(this.data.cainacnt == 1) {
      this.setData({
        accept: true
      })
      this.data.cainacnt = 0
      app.globalData.items[this.data.index]['match'] = parseInt(app.globalData.items[this.data.index]['match']) + 1
    } else {
      wx.showToast({
        title: '请勿重复采纳',
        icon: 'none'
      })
    }
  },
  onHide: function(e) {
    innerAudioContext.stop()
  },
  onUnload() {
    innerAudioContext.stop()
  }
})