from tempfile import tempdir
from turtle import color
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sb

# st.sidebar.header("Team name:")
# st.sidebar.subheader("       Aman")
with open("like_count.txt","r") as f:
    count = f.read()
st.sidebar.title("Whats app chat analyzer")

if st.sidebar.button('Like'):
    count = int(count) + 1
    with open('like_count.txt','w') as f:
        f.write(str(count))
    st.sidebar.write(str(count))
    
   

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # FOR NOT PRINT DATA FRAME***************||
    # st.dataframe(df)

    
    

    #unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("All Member here ",user_list)
    if st.sidebar.button("Show Analysis"):
            
        st.title("Top statistics")
        

        num_messages , words , num_media_messages ,num_links =  helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)

        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media_messages) 
        with col4:
            st.header("Links Shared")
            st.title(num_links)  

        # MONTHLY___TIMELINE HERE *********************
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # DAILY TIMELINe ****************
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #MOST ACTIVE USER IN THIS DAYS&***************
        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color="brown")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            busy_month = helper.monthly_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="orange")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # ONLINE PERSON ********************
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sb.heatmap(user_heatmap)
        st.pyplot(fig)


        #FINDING THE BUSIEST USERS IN THE GROUP:::
        if selected_user =='Overall':
            st.title('Most busy User')
            x , new_df = helper.most_busy_user(df)
            fig,ax = plt.subplots()
            
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        # WORDCLOUD
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user,df) 
        fig,ax = plt.subplots()
        ax.imshow(df_wc)      
        st.pyplot(fig) 

        #MOST COMMON WORDS ************************
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()

        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation = 'vertical')
        st.title('Most common words')
        st.pyplot(fig )

        # EMOJI ***************************
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji analysis")

        col1,col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig.ax =  plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig) 
        # st.title("Organizes Whats  App Chat")
        # st.dataframe(df)

                 
         