package com.example.oneteaapp.wxapi.util;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.Handler;
import android.os.Message;
import android.text.TextUtils;
import android.util.Log;
import com.alipay.sdk.app.PayTask;
import com.example.oneteaapp.R;
import com.example.oneteaapp.wxapi.WXPayEntryActivity;
import com.tencent.mm.opensdk.modelmsg.SendMessageToWX;
import com.tencent.mm.opensdk.modelmsg.WXMediaMessage;
import com.tencent.mm.opensdk.modelmsg.WXWebpageObject;
import com.tencent.mm.opensdk.modelpay.PayReq;
import com.tencent.mm.opensdk.openapi.IWXAPI;
import com.tencent.mm.opensdk.openapi.WXAPIFactory;
import java.util.Map;

public class WeiXinConstants {
    // APP_ID 替换为你的应用从官方网站申请到的合法appId
   public static final String APP_ID = "wxcf6ea6e0b71b8132";

//    private IWXAPI iwxapi; //微信支付api
//
//    private void regToWx() {
//        iwxapi = WXAPIFactory.createWXAPI(this, WeiXinConstants.APP_ID);
//        // 将该app注册到微信
//        iwxapi.registerApp(WeiXinConstants.APP_ID);
//    }

//    private void sharewx(int type) {//分享到微信
//        WXWebpageObject webpage = new WXWebpageObject();
//        webpage.webpageUrl = "http://app.fgpa.com/view/html/zhuce.html?pid=" + Global.getId();//分享的链接
//        WXMediaMessage msg = new WXMediaMessage(webpage);
//        msg.title = "全球鹦";//主标题
//        msg.description = "全球鹦全球鹦全球鹦全球鹦全球鹦全球鹦全球鹦";//副标题
//        Bitmap thumbBmp = BitmapFactory.decodeResource(getResources(), R.mipmap.baobaoxinxi3);
//        msg.thumbData = Bitmap2Bytes(thumbBmp);
//        SendMessageToWX.Req req = new SendMessageToWX.Req();
//        if (type == 1) {
//            req.scene = SendMessageToWX.Req.WXSceneSession;//分享到对话
//        } else if (type == 2) {
//            req.scene = SendMessageToWX.Req.WXSceneTimeline;//分享到朋友圈
//        }
//        req.message = msg;
//        iwxapi.sendReq(req);
//    }


//    PayReq request = new PayReq(); //调起微信APP的对象
//    request.appId = "" + WeiXinConstants.APP_ID;
//    request.partnerId = "" + object.getData().getPartnerid();
//    request.prepayId = "" + object.getData().getPrepayid();
//    request.packageValue = "" + "Sign=WXPay";
//    request.nonceStr = "" + object.getData().getNoncestr();
//    request.timeStamp = "" + object.getData().getTimestamp();
//    request.sign = "" + object.getData().getSign();
//                iwxapi.sendReq(request);//发送调起微信的请求


//    private Handler mHandler = new Handler() {
//        @SuppressWarnings("unused")
//        public void handleMessage(Message msg) {
//            switch (msg.what) {
//                case 1: {
//                    @SuppressWarnings("unchecked")
//                    PayResult payResult = new PayResult((Map<String, String>) msg.obj);
//                    /**
//                     对于支付结果，请商户依赖服务端的异步通知结果。同步通知结果，仅作为支付结束的通知。
//                     */
//                    String resultInfo = payResult.getResult();// 同步返回需要验证的信息
//                    String resultStatus = payResult.getResultStatus();
//                    // 判断resultStatus 为9000则代表支付成功
//                    if (TextUtils.equals(resultStatus, "9000")) {
//                        // 该笔订单是否真实支付成功，需要依赖服务端的异步通知。
//                        //  PaySuccessActivity.actionStart(BuyOrRentActivity.this);
//                        WebviewByHtmlActivity.actionStart(BuyOrRentActivity.this,"设备订单");
//                        finish();
//                    } else {
//                        // 该笔订单真实的支付结果，需要依赖服务端的异步通知。
//                        showShortTip("支付失败");
//                    }
//                    break;
//                }
//            }
//        }
//    };


//    private void paystart(final String info) {
//        Log.e("info", info);
//        Runnable payRunnable = new Runnable() {
//            @Override
//            public void run() {
//                Log.e("info", info);
//                PayTask alipay = new PayTask(BuyOrRentActivity.this);
//                Map<String, String> result = alipay.payV2(info, true);
//                Message msg = new Message();
//                msg.what = 1;
//                msg.obj = result;
//                mHandler.sendMessage(msg);
//            }
//        };
//        // 必须异步调用
//        Thread payThread = new Thread(payRunnable);
//        payThread.start();
//    }
}