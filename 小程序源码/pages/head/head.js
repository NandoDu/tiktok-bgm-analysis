const app = getApp()

Page({
  onLoad() {
  },
  onShow() {
    var that = this
    wx.request({
      url: 'https://nandodu-blog.oss-cn-shanghai.aliyuncs.com/%E6%8A%96%E9%9F%B3%E9%9F%B3%E9%A2%91%E6%95%B0%E6%8D%AE%E5%BA%93/base.json',
      success(res) {
        var size = that.JSONLength(res.data)
        var items = []
        var indexList = that.randomDiffNum(size)
        for (var i in indexList) {
          res.data[i]['bpm'] = Math.round(parseFloat(res.data[i]['bpm']))
          items.push(res.data[i])
        }
        app.globalData.items = items
        setTimeout(function() {
          wx.redirectTo({
            url: '/pages/index/index'
          })
        }, 5000)
      }
    })
  },
  JSONLength: function (obj) {
    var size = 0;
    var key;
    for (key in obj) {
      if (obj.hasOwnProperty(key))
        size++;
    }
    return size;
  },
  randomDiffNum: function(n){
    var num = [];
    for(var i = 0; i< 800; i++){
      num[i] = Math.floor(Math.random() * n);
      for (var j = 0; j < i; j++) {
        if (num[i] == num[j]) {
          i--;
        }
      }
    }
    return num;
  }
})