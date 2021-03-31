const app = getApp()

Page({
  data: {
    array: ['食品类','美妆类','服装类','电器数码类','医药保健类','家装日用类','文具玩具图书类','鞋靴箱包饰品类','其他'],
    index: 0,
    pickerHid: false,
    type: 0,
  },
  onLoad: function(e) {
  },
  onShow: function(e) {
  },
  bindPickerChange: function (e) {
    if(e.detail.value == 0) {
      this.setData({
        items: app.globalData.items.sort(this.upF),
        type: 0
      })
    } else if(e.detail.value == 7) {
      this.setData({
        items: app.globalData.items.sort(this.upS),
        type: 7
      })
    } else if (e.detail.value == 1) {
      this.setData({
        items: app.globalData.items.sort(this.upM),
        type: 1
      })
    } else if (e.detail.value == 3) {
        this.setData({
          items: app.globalData.items.sort(this.upE),
          type: 3
        })
    } else if (e.detail.value == 2) {
        this.setData({
          items: app.globalData.items.sort(this.upC),
          type: 2
        })
    } else if (e.detail.value == 6) {
        this.setData({
          items: app.globalData.items.sort(this.upW),
          type: 6
        })
    } else if (e.detail.value == 5) {
        this.setData({
          items: app.globalData.items.sort(this.upR),
          type: 5
        })
    } else if (e.detail.value == 4) {
        this.setData({
          items: app.globalData.items.sort(this.upY),
          type: 4
        })
    } else if (e.detail.value == 8) {
      this.setData({
        items: app.globalData.items.sort(this.upQ),
        type: 8
      })
    }
    this.setData({
      pickerHid: true
    })
  },
  turnToMusic:function(e) {
    console.log(this.data.items[index])
    var index = e.currentTarget.dataset.index
    var goodsType = this.data.array[this.data.type]
    var musicData = this.data.items[index][goodsType]
    var rankIndex = musicData.indexOf(',')
    var languageIndex = musicData.lastIndexOf('language') + 11
    var emotionIndex = musicData.lastIndexOf('emotion') + 10
    var bpmIndex = musicData.lastIndexOf('bpm') + 6
    var public_timeIndex = musicData.lastIndexOf('public_time') + 14
    var genreIndex = musicData.lastIndexOf('genre') + 8
    var attitudeIndex = musicData.lastIndexOf('attitude') + 11
    var rank = musicData.substr(1, rankIndex - 1)
    var language = musicData.substr(languageIndex).substr(0, musicData.substr(languageIndex).indexOf(','))
    var emotion = musicData.substr(emotionIndex).substr(0, musicData.substr(emotionIndex).indexOf(','))
    var bpm = musicData.substr(bpmIndex).substr(0, musicData.substr(bpmIndex).indexOf(','))
    var public_time = musicData.substr(public_timeIndex).substr(0, musicData.substr(public_timeIndex).indexOf(','))
    var genre = musicData.substr(genreIndex).substr(0, musicData.substr(genreIndex).indexOf(','))
    var attitude = musicData.substr(attitudeIndex).substr(0, musicData.substr(attitudeIndex).indexOf('}'))
    var name = this.data.items[index]['bgm']
    var languageInfo = this.data.items[index]['language']
    var emotionInfo = this.data.items[index]['emotion']
    var bpmInfo = this.data.items[index]['bpm']
    var genreInfo = this.data.items[index]['genre']
    var attitudeInfo = this.data.items[index]['attitude']
    var public_timeInfo = this.data.items[index]['public_time']
    var match = this.data.items[index]['match']
    var like_time = this.data.items[index]['like_time']
    var unlike_time = this.data.items[index]['unlike_time']
    var that = this
    var filename = this.data.items[index]['filename']
    wx.navigateTo({
      url: '/pages/musicPlayer/musicPlayer?rank=' + rank + '&language=' + language + '&emotion=' + emotion + '&bpm=' + bpm + '&public_time=' + public_time + '&genre=' + genre + '&attitude=' + attitude + '&name=' + name + '&goodsType=' + goodsType + '&attitudeInfo=' + attitudeInfo + '&languageInfo=' + languageInfo + '&match=' + match + '&like_time=' + like_time + '&unlike_time=' + unlike_time + '&genreInfo=' + genreInfo + '&bpmInfo=' + bpmInfo + '&emotionInfo=' + emotionInfo + '&public_timeInfo=' + public_timeInfo + '&index=' + index + '&filename=' + filename
    })
  },
  backToPicker: function(e) {
    this.setData({
      pickerHid: false,
      items: []
    })
  },
  JSONLength: function(obj) {
    var size = 0;
    var key;
    for(key in obj) {
      if (obj.hasOwnProperty(key))
        size++;
    }
    return size;
  },
  upF: function(x, y) {
    var index1 = (x.食品类).indexOf(',')
    var t1 = (x.食品类).substr(1, index1 - 1)
    var index2 = (y.食品类).indexOf(',')
    var t2 = (y.食品类).substr(1, index2 - 1)
    return t1 - t2
  },
  upS: function(x, y) {
    var index1 = (x.鞋靴箱包饰品类).indexOf(',')
    var t1 = (x.鞋靴箱包饰品类).substr(1, index1 - 1)
    var index2 = (y.鞋靴箱包饰品类).indexOf(',')
    var t2 = (y.鞋靴箱包饰品类).substr(1, index2 - 1)
    return t1 - t2
  },
  upM: function(x, y) {
    var index1 = (x.美妆类).indexOf(',')
    var t1 = (x.美妆类).substr(1, index1 - 1)
    var index2 = (y.美妆类).indexOf(',')
    var t2 = (y.美妆类).substr(1, index2 - 1)
    return t1 - t2
  },
  upE: function(x, y) {
    var index1 = (x.电器数码类).indexOf(',')
    var t1 = (x.电器数码类).substr(1, index1 - 1)
    var index2 = (y.电器数码类).indexOf(',')
    var t2 = (y.电器数码类).substr(1, index2 - 1)
    return t1 - t2
  },
  upC: function(x, y) {
    var index1 = (x.服装类).indexOf(',')
    var t1 = (x.服装类).substr(1, index1 - 1)
    var index2 = (y.服装类).indexOf(',')
    var t2 = (y.服装类).substr(1, index2 - 1)
    return t1 - t2
  },
  upW: function(x, y) {
    var index1 = (x.文具玩具图书类).indexOf(',')
    var t1 = (x.文具玩具图书类).substr(1, index1 - 1)
    var index2 = (y.文具玩具图书类).indexOf(',')
    var t2 = (y.文具玩具图书类).substr(1, index2 - 1)
    return t1 - t2
  },
  upR: function(x, y) {
    var index1 = (x.家装日用类).indexOf(',')
    var t1 = (x.家装日用类).substr(1, index1 - 1)
    var index2 = (y.家装日用类).indexOf(',')
    var t2 = (y.家装日用类).substr(1, index2 - 1)
    return t1 - t2
  },
  upY: function(x, y) {
    var index1 = (x.医药保健类).indexOf(',')
    var t1 = (x.医药保健类).substr(1, index1 - 1)
    var index2 = (y.医药保健类).indexOf(',')
    var t2 = (y.医药保健类).substr(1, index2 - 1)
    return t1 - t2
  },
  upQ: function(x, y) {
    var index1 = (x.其他).indexOf(',')
    var t1 = (x.其他).substr(1, index1 - 1)
    var index2 = (y.其他).indexOf(',')
    var t2 = (y.其他).substr(1, index2 - 1)
    return t1 - t2
  }
})